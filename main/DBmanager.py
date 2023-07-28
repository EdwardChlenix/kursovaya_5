import psycopg2

class DBManager:

    def __init__(self, params: dict):
        self.params = params

    def get_companies_and_vacancies_count(self):
        conn = psycopg2.connect(database='hh_parser', **self.params)
        cur = conn.cursor()

        cur.execute("""SELECT title_company, number_vacancies FROM company""")
        rows = cur.fetchall()

        for i in rows:
            name_company = i[0]
            count_vacancy = i[1]
            print(f'{name_company}: Количество вакансий - {count_vacancy}')
        cur.close()
        conn.close()

    def get_all_vacancies(self):
        conn = psycopg2.connect(database='hh_parser', **self.params)
        cur = conn.cursor()

        cur.execute("""SELECT  title_company, vacancy_name, salary_from, salary_to, alternate_url
                        FROM company_vacancies
                        INNER JOIN company USING (company_id)""")

        rows = cur.fetchall()

        for i in rows:
            name_company = i[0]
            name_vacancy = i[1]
            salary_from = i[2]
            salary_to = i[3]
            url_vacancy = i[4]
            print()
            print(f'Название компании: {name_company}'
                  f'\nНазвание вакансии: {name_vacancy}'
                  f'\nЗарплата: c {salary_from} до {salary_to} руб.'
                  f'\nСсылка на вансию: {url_vacancy}')
        cur.close()
        conn.close()

    def get_avg_salary(self):
        conn = psycopg2.connect(database='hh_parser', **self.params)
        cur = conn.cursor()

        cur.execute("""
                    SELECT title_company, ROUND(AVG(salary_from))
                    FROM company_vacancies 
                    INNER JOIN company USING (company_id)
                    WHERE salary_from > 0
                    GROUP BY title_company
                    """)

        rows = cur.fetchall()

        for i in rows:
            name_company = i[0]
            avg_salary = i[1]
            print(f'Средняя зарплата в компании {name_company} - {avg_salary} руб.')

        cur.close()
        conn.close()

    def get_vacancies_with_higher_salary(self):
        conn = psycopg2.connect(database='hh_parser', **self.params)
        cur = conn.cursor()

        cur.execute("""
                    SELECT vacancy_name
                    FROM company_vacancies
                    WHERE salary_from > (SELECT AVG(salary_from) FROM company_vacancies)
                    """)

        rows = cur.fetchall()
        print(f'Список вакансий, у которых зарплата выше средней по всем вакансиям:')
        for i in rows:
            name_company_avg = i[0]
            print(name_company_avg)

        cur.close()
        conn.close()

    def get_vacancies_with_keyword(self, user_word):

        conn = psycopg2.connect(database='hh_parser', **self.params)
        cur = conn.cursor()
        cur.execute(f""" 
                    SELECT vacancy_name
                    FROM company_vacancies
                    WHERE vacancy_name ILIKE '%{user_word}%'
                    """)
        rows = cur.fetchall()
        if rows == []:
            print('По данному ключевому слову не найдено вакансий')
        else:
            print(f'Список вакансий, у которых в названии имеется слово "{user_word}"')
            for i in rows:
                name_company = i[0]
                print(name_company)

        cur.close()
        conn.close()
