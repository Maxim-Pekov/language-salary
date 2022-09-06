import requests
from get_rub_salary import get_rub_salary

from environs import Env


URL = 'https://api.hh.ru/vacancies'


def get_count_vacancies(params, headers):
    response = requests.get(URL, headers=headers, params=params)
    response.raise_for_status()
    vacancies_json = response.json()
    count_vacancies = vacancies_json.get('found')
    return count_vacancies


def get_rub_salary(vacancy):
    if not vacancy.get('salary'):
        return None
    salary_from = vacancy['salary']['from']
    salary_to = vacancy['salary']['to']
    if vacancy.get('salary').get('currency') == 'RUR':
        rub_salary = get_rub_salary(salary_from, salary_to)
        return rub_salary


def get_information_vacancies_by_language(language, email):
    information_by_language = {}
    page = 0
    pages = 1
    vacancies = []
    all_salaries = []
    params = {
        'text': f'программист {language}',
        'area': 1,   # Moscow id
        'page': page
    }
    headers = {
        'User-Agent': f'MyHH_MaxPek/1.0 ({email})'
    }
    while page < pages:
        response = requests.get(URL, headers=headers, params=params)
        response.raise_for_status()
        vacancies_information = response.json()
        vacancies += vacancies_information.get('items')
        pages = vacancies_information.get('pages')
        page += 1
    for vacancy in vacancies:
        if rub_salary := get_rub_salary(vacancy):
            all_salaries.append(rub_salary)
    vacancies_count = vacancies_information.get('found')
    information_by_language['found_vacancies'] = vacancies_count
    information_by_language['processed_vacancies'] = len(all_salaries)
    if all_salaries:
        information_by_language['average_salary'] = int(sum(all_salaries) / len(all_salaries))
    else:
        information_by_language['average_salary'] = 0
    return information_by_language


def get_salary_information_by_languages(email):
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'C', 'C++', 'C#', 'Go', 'PHP', 'Objective-C', 'Scala', 'Swift']
    average_salaries = {}
    for language in languages:
        average_salaries[language] = get_information_vacancies_by_language(language, email)
    return average_salaries


def main():
    env = Env()
    env.read_env()
    email = env.str('EMAIL')
    get_salary_information_by_languages(email)


if __name__ == '__main__':
    main()


