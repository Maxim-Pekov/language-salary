import requests

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
    if vacancy.get('salary').get('currency') == 'RUR':
        if vacancy['salary']['from'] and vacancy['salary']['to']:
            return (vacancy['salary']['from'] + vacancy['salary']['to']) // 2
        elif vacancy['salary']['from'] and not vacancy['salary']['to']:
            return vacancy['salary']['from'] * 1.2
        elif vacancy['salary']['to'] and not vacancy['salary']['from']:
            return vacancy['salary']['to'] * 0.8
        else:
            return None


def get_information_vacancies_by_language(language, email):
    information_by_language = {}
    all_salaries = []
    page = 0
    pages = 1
    vacancies = []
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
    all_salaries = [get_rub_salary(vacancy) for vacancy in vacancies if get_rub_salary(vacancy)]
    count_vacancies = response.json().get('found')
    information_by_language['vacancies_found'] = count_vacancies
    information_by_language['vacancies_processed'] = len(all_salaries)
    information_by_language['average_salary'] = int(sum(all_salaries) / len(all_salaries))
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


