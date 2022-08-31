from terminaltables import AsciiTable
import fetch_average_super_job_salary
import fetch_average_head_hunter_salary


def print_table(data, name):
    title = name
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]
    for i in data:
        table_data.append([i, data[i]['vacancies_found'], data[i]['vacancies_processed'], data[i]['average_salary']], )
    table_instance = AsciiTable(table_data, title)
    for i in range(4): table_instance.justify_columns[i] = 'center'
    print(table_instance.table)
    print()


def main():
    super_job_data = fetch_average_super_job_salary.get_salary_information_by_languages()
    head_hunter_data = fetch_average_head_hunter_salary.get_salary_information_by_languages()
    print_table(super_job_data, f'Super Job Moscow')
    print_table(head_hunter_data, f'Head Hunter Moscow')


if __name__ == '__main__':
    main()
