from pprint import pprint

import requests
from environs import Env

def main():
    env = Env()
    env.read_env()
    x = env.str('SECRET_KEY_SUPER_JOB')
    url = 	'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id' : x}
    response = requests.get(url, headers=headers)
    # pprint(response.json())
    z = response.json()
    for i in z['objects']:
        print(i['profession'])


if __name__ == '__main__':
    main()
