import requests
import psycopg2

def headhunter_data(company_ids: list[str]):
    data = []
    for company_id in company_ids:
        url_company = f'https://api.hh.ru/employers/{company_id}'
        url_vacancy = 'https://api.hh.ru/vacancies'
        params = {'employer_id': company_id,
                  'per_page': '10'}
        headers = {"User-Agent": "322322", }
        response_vacancy = requests.get(url_vacancy, params=params, headers=headers)
        response_company = requests.get(url_company, headers=headers)

        if response_vacancy.status_code == 200 and response_company.status_code == 200:
            data_vacancy = response_vacancy.json()
            dat_company = response_company.json()
            data.append({'company': dat_company, 'vacancy': data_vacancy['items']})
        else:
            print('Ошибка при подключении')
    return data


def create_database(database_name: str, params: dict):

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name} WITH (FORCE)")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE company (
                company_id SERIAL PRIMARY KEY,
                title_company VARCHAR(255),
                number_vacancies INTEGER
            );
            CREATE TABLE company_vacancies (
                vacancy_name TEXT,
                company_id INT REFERENCES company(company_id),
                salary_from INTEGER,
                salary_to INTEGER,
                alternate_url TEXT
            );
        """)

    conn.commit()
    conn.close()

def save_data_to_database(data: list[dict[str, ]], database_name: str, params: dict):

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in data:
            company_id = company['company']['id']
            title_company = company['company']['name']
            number_vacancies = company['company']['open_vacancies']
            cur.execute(
                """
                INSERT INTO  company (company_id, title_company, number_vacancies)
                VALUES (%s, %s, %s)
                """,
                (company_id, title_company, number_vacancies)
            )
            for vacancy in company['vacancy']:
                vacancy_name = vacancy['name']

                if vacancy['salary'] is not None:
                    if vacancy['salary']['from'] is not None:
                        salary_from = vacancy['salary']['from']
                    else:
                        salary_from = vacancy['salary']['to']
                    if vacancy['salary']['to'] is not None:
                        salary_to = vacancy['salary']['to']
                    else:
                        salary_to = vacancy['salary']['from']
                else:
                    salary_from = 0
                    salary_to = 0

                url_vacancy = vacancy['alternate_url']
                cur.execute(
                    """
                    INSERT INTO company_vacancies (company_id, vacancy_name, salary_from, salary_to, alternate_url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (company_id, vacancy_name, salary_from, salary_to, url_vacancy)
                )

    conn.commit()
    conn.close()
