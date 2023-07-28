from headhunter import headhunter_data, create_database, save_data_to_database
from DBmanager import DBManager
from config import config

def main():
    params = config()
    while True:
        user_input = input("Введите ID интересующих вас компаний (через пробел): ")
        company_ids = [item for item in user_input.split()]
        if company_ids:
            data = headhunter_data(company_ids)
            create_database('hh_parser', params)
            save_data_to_database(data, 'hh_parser', params)
            if data:
                break
            else:
                print('Не существующие ID компаний, попробуйте еще раз.')
                continue
        elif user_input == 'cnjg' or user_input == 'стоп' or user_input == 'stop':
            quit()
        else:
            print('Вы ничего не ввели, попробуйте еще раз. Пропишите "стоп" если хотите остановить программу')






    information = DBManager(params)

    while True:
        user_call = input('Выберите то, что хотите посмотреть.\n'
                          '1 - список всех компаний и количество вакансий у каждой\n'
                          '2 - список вакансий, название компании, зп, ссылка на вакансию\n'
                          '3 - показать среднюю зп по вакансиям\n'
                          '4 - вакансии с зп выше среднего по всем вакансиям\n'
                          '5 - вакансии со словом ключевому слову\n'
                          'Для выхода введи стоп\n')

        if user_call == '1':
            information.get_companies_and_vacancies_count()
            next_ques = input("Показать что-нибудь еще?\n")
            if next_ques.lower() == 'да' or next_ques.lower() == 'lf' or next_ques.lower() == '':
                continue
            else:
                break

        elif user_call == '2':
            information.get_all_vacancies()
            next_ques = input("Показать что-нибудь еще?\n")
            if next_ques.lower() == 'да' or next_ques.lower() == 'lf' or next_ques.lower() == '':
                continue
            else:
                break


        elif user_call == '3':
            information.get_avg_salary()
            next_ques = input("Показать что-нибудь еще?\n")
            if next_ques.lower() == 'да' or next_ques.lower() == 'lf' or next_ques.lower() == '':
                continue
            else:
                break

        elif user_call == '4':
            information.get_vacancies_with_higher_salary()
            next_ques = input("Показать что-нибудь еще?\n")
            if next_ques.lower() == 'да' or next_ques.lower() == 'lf' or next_ques.lower() == '':
                continue
            else:
                break

        elif user_call == '5':
            word = input("Введите ключевое слово: ")
            information.get_vacancies_with_keyword(word)
            next_ques = input("Показать что-нибудь еще?\n")
            if next_ques.lower() == 'да' or next_ques.lower() == 'lf' or next_ques.lower() == '':
                continue
            else:
                break

        elif user_call == 'stop' or user_call == 'cnjg' or user_call == 'стоп':
            break

        else:
            continue

if __name__ == '__main__':
    main()
