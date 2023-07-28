--получение списка всех компаний и кол-во их вакансий
SELECT title_company, number_vacancies FROM company

--получение названий всех вакансий и зарплаты с ссылкой на вакансию
SELECT  title_company, vacancy_name, salary_from, salary_to, alternate_url
FROM company_vacancies
INNER JOIN company USING (company_id)

--получение средней зарплаты по вакансиям
SELECT title_company, ROUND(AVG(salary_from))
FROM company_vacancies
INNER JOIN company USING (company_id)
WHERE salary_from > 0
GROUP BY title_company

--получение списка всех вакансий, у которых зарплата выше средней
SELECT vacancy_name
FROM company_vacancies
WHERE salary_from > (SELECT AVG(salary_from) FROM company_vacancies)

--получение списка всех вакансий по ключевому слову
SELECT vacancy_name
FROM company_vacancies
WHERE vacancy_name ILIKE '%PYTHON%'
--заменить PYTHON на интересующее слово