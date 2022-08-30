import requests

from environs import Env
from pprint import pprint


env = Env()
env.read_env()
email = env.str('EMAIL')

headers = {
    'User-Agent': f'MyHH_MaxPek/1.0 ({email})'
}

url = 'https://api.hh.ru/vacancies'


def get_count_vacancies(language):
    params = {
        'text': f'программист {language}',
        'area': 1    # index by Moscow
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    z = response.json()
    return z.get('found')

# def salary(language):
#     params = {
#         'text': f'программист {language}',
#         'area': 1
#     }
#     response = requests.get(url, headers=headers, params=params)
#     response.raise_for_status()
#     z = response.json()
#     average_salary = []
#     num = 0
#     for numerate, x in enumerate(z['items']):
#         if predict_rub_salary(x):
#             average_salary.append(predict_rub_salary(x))
#             num = numerate
#         pprint(x['salary'])
#         pprint(predict_rub_salary(x))
#     print(sum(average_salary)/num)
#     print()
#     # print([get_count_vacancy(language), num, (average_salary)])


def predict_rub_salary(x):
    if not x.get('salary'):
        return None
    if x.get('salary').get('currency') == 'RUR':
        if x['salary']['from'] and x['salary']['to']:
            return (x['salary']['from'] + x['salary']['to']) // 2
        elif x['salary']['from'] and not x['salary']['to']:
            return x['salary']['from'] * 1.2
        elif x['salary']['to'] and not x['salary']['from']:
            return x['salary']['to'] * 0.8
        else:
            return None
    return None


def get_information_by_language(language):
    information_by_language = {}
    all_salaries = []
    page = 0
    pages = 1
    vacancies = []
    params = {
        'text': f'программист {language}',
        'area': 1,
        'page': page
    }
    while page < pages:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        z = response.json()
        # print(len(vacancies))
        vacancies += z['items']
        pages = z['pages']
        page += 1
    for x in vacancies:
        if predict_rub_salary(x):
            all_salaries.append(predict_rub_salary(x))
    information_by_language['vacancies_found'] = get_count_vacancies(language)
    information_by_language['vacancies_processed'] = len(all_salaries)
    information_by_language['average_salary'] = int(sum(all_salaries) / len(all_salaries))

    return information_by_language


def get_information_by_languages():
    # languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'C', 'C++', 'C#', 'Go', 'PHP', 'Objective-C', 'Scala', 'Swift']
    languages = ['Python', 'Java']
    avarage_salaries = {}
    for language in languages:
        avarage_salaries[language] = get_information_by_language(language)
    pprint(avarage_salaries)
    return avarage_salaries


if __name__ == '__main__':
    get_information_by_languages()

