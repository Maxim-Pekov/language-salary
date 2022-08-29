from pprint import pprint

import requests

headers = {
    'User-Agent': 'MyHH_MaxPek/1.0 (MM)'
}
url = 'https://api.hh.ru/vacancies'

def x():
    response = requests.get('https://api.hh.ru/areas/2')
    pprint(response.json())
def main(q):
    params = {
        'text': f'программист {q}',
        'area': 2
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    z = response.json()
    # pprint(z['items'][0]['salary'])
    count = 0
    # print()
    # for s in z['items']:
    #     if s['published_at'] > '2022-07-27':
    #         count += 1
    #         pprint(s['created_at'])
    # pprint(z['items'][0]['created_at'])
    # print(count)
    return z['found']

def salary(language):
    params = {
        'text': f'программист {language}',
        'area': 1
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    z = response.json()
    for x in z['items']:
        pprint(x['salary'])
        pprint(predict_rub_salary(x))



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

if __name__ == '__main__':
    slovar = {}
    w = ['Python', 'Java', 'JavaScript', 'Ruby', 'C', 'C++', 'C#', 'Go', 'PHP', 'Objective-C', 'Scala', 'Swift']
    for q in w:
        slovar[q] = main(q)
    pprint(slovar)
    x()
    salary('python')
    # main()


