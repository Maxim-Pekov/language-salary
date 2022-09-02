from terminaltables import AsciiTable
import fetch_average_super_job_salary
import fetch_average_head_hunter_salary


def print_table(average_salaries, table_name):
    title = table_name
    table_headers = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]
    for average_salary in average_salaries:
        table_headers.append([average_salary, average_salaries[average_salary]['vacancies_found'],
                              average_salaries[average_salary]['vacancies_processed'],
                              average_salaries[average_salary]['average_salary']], )
    table_instance = AsciiTable(table_headers, title)
    for _ in range(4): table_instance.justify_columns[_] = 'center'
    print(table_instance.table)
    print()


def main():
    super_job_average_salaries = fetch_average_super_job_salary.get_salary_information_by_languages()
    head_hunter_average_salaries = fetch_average_head_hunter_salary.get_salary_information_by_languages()
    print_table(super_job_average_salaries, f'Super Job Moscow')
    print_table(head_hunter_average_salaries, f'Head Hunter Moscow')


if __name__ == '__main__':
    main()
