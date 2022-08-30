from pprint import pprint

import requests
from environs import Env


def predict_rub_salary_for_superJob(y):
    # pprint(y)
    from_ = int(y['payment_from'])
    to_ = int(y['payment_to'])
    if not y:
        return None
    if from_ and to_:
        return (from_ + to_) // 2
    elif from_ and not to_:
        return from_ * 1.2
    elif to_ and not from_:
        return to_ * 0.8
    else:
        return None
    return None


def get_information_by_language(language):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    env = Env()
    env.read_env()
    x = env.str('SECRET_KEY_SUPER_JOB')
    headers = {'X-Api-App-Id' : x}
    information_by_language = {}
    all_salaries = []
    vacancies = []
    params = {
        'town': 'Moscow',
        'keyword': f'программирование, {language}',
        'count': 100,
        'page': 5
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    z = response.json()
    # pprint(z)
    vacancies += z['objects']
    for x in vacancies:
        if predict_rub_salary_for_superJob(x):
            all_salaries.append(predict_rub_salary_for_superJob(x))
    information_by_language['vacancies_found'] = z['total']
    information_by_language['vacancies_processed'] = len(all_salaries)
    if len(all_salaries) != 0:
        information_by_language['average_salary'] = int(sum(all_salaries) / len(all_salaries))
    else:
        information_by_language['average_salary'] = 0
    return information_by_language


def get_information_by_languages():
    # languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'C', 'C++', 'C#', 'Go', 'PHP', 'Objective-C', 'Scala', 'Swift']
    languages = ['Python', 'Java']
    avarage_salaries = {}
    for language in languages:
        avarage_salaries[language] = get_information_by_language(language)
    # pprint(avarage_salaries)
    return avarage_salaries


def main():
    env = Env()
    env.read_env()
    x = env.str('SECRET_KEY_SUPER_JOB')
    params = {
        'town': 'Moscow',
        'keyword': 'Разработка, программирование',
        'count': 100
    }
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id' : x}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    # pprint(response.json())
    z = response.json()
    pprint(z)
    for i in z['objects']:
        salary = predict_rub_salary_for_superJob(i)
        # print(f"{i['profession']} - {i['town']['title']} - {salary}")


if __name__ == '__main__':
    get_information_by_languages()
    # main()
