from terminaltables import AsciiTable, SingleTable, DoubleTable
import super_job
import main

z = super_job.get_information_by_languages()
hh = main.get_information_by_languages()



def print_table(data, name):
    title = name
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]
    for i in data:
        table_data.append([i, data[i]['vacancies_found'], data[i]['vacancies_processed'], data[i]['average_salary']], )
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'center'
    print(table_instance.table)
    print()



def main():
    print_table(z, 'Super Job Moscow')
    print_table(hh, 'Head Hunter Moscow')


if __name__ == '__main__':
    main()
