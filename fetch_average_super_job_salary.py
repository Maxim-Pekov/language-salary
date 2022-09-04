import requests
from environs import Env


TOWN = 'Moscow'
URL = 'https://api.superjob.ru/2.0/vacancies/'

def get_rub_salary(vacancy):
    from_ = int(vacancy.get('payment_from'))
    to_ = int(vacancy.get('payment_to'))
    if not vacancy:
        return None
    if from_ and to_:
        return (from_ + to_) // 2
    elif from_ and not to_:
        return from_ * 1.2
    elif to_ and not from_:
        return to_ * 0.8
    else:
        return None


def get_information_vacancies_by_language(language, secret_key):
    headers = {'X-Api-App-Id': secret_key}
    information_by_language = {}
    all_salaries = []
    vacancies = []
    items_in_page = 100
    params = {
        'town': TOWN,
        'keyword': f'программирование, {language}',
        'count': items_in_page,
        'page': 5
    }
    response = requests.get(URL, headers=headers, params=params)
    response.raise_for_status()
    vacancies_information = response.json()
    vacancies += vacancies_information.get('objects')
    for vacancy in vacancies:
        if get_rub_salary(vacancy):
            all_salaries.append(get_rub_salary(vacancy))
    information_by_language['vacancies_found'] = vacancies_information['total']
    information_by_language['vacancies_processed'] = len(all_salaries)
    if len(all_salaries) != 0:
        information_by_language['average_salary'] = int(sum(all_salaries) / len(all_salaries))
    else:
        information_by_language['average_salary'] = 0
    return information_by_language


def get_salary_information_by_languages(secret_key):
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'C', 'C++', 'C#', 'Go', 'PHP', 'Objective-C', 'Scala', 'Swift']
    average_salaries = {}
    for language in languages:
        average_salaries[language] = get_information_vacancies_by_language(language, secret_key)
    return average_salaries


def main():
    env = Env()
    env.read_env()
    secret_key = env.str('SECRET_KEY_SUPER_JOB')
    print(get_salary_information_by_languages(secret_key))


if __name__ == '__main__':
    main()

