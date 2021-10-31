from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import requests
from bs4 import BeautifulSoup as bs

client = MongoClient('localhost', 27017)
db = client['testdb']
vacancies = db.vacancies
url = 'https://hh.ru'


def write_vacs(vacname,pages):
    while True:
        response = requests.get(url + '/search/vacancy', params = params, headers = headers)
        soup = bs(response.text, 'html.parser')
        vacs = soup.find_all('div', {'class': 'vacancy-serp-item'})
        if response.ok and vacs and params['page'] < int(pages):
            for vac in vacs:
                vac_data = {}
                info = vac.find('a', {'class': 'bloko-link'})
                name = info.text
                salary_block = vac.find('div', {'class': 'vacancy-serp-item__sidebar'})
                link = info['href']
                try:
                    salary = salary_block.find('span').text
                    salary = salary.replace("\u202f","")
                    if salary.startswith("от",0,3):
                        salary_min = int(salary.split()[1])
                        salary_max = "Не указано"
                        salary_zcurrency = ''.join(salary.split()[2:])
                    elif "до" in salary:
                        salary_min = "Не указано"
                        salary_max = int(salary.split()[1])
                        salary_zcurrency = ''.join(salary.split()[2:])
                    else:
                        salary_min = int(salary.split()[0])
                        salary_max = int(salary.split()[2])
                        salary_zcurrency = ''.join(salary.split()[3:])
                except:
                    salary_min = 'Не указано'
                    salary_max = 'Не указано'
                    salary_zcurrency = 'Не указано'
                vac_data['name'] = name
                vac_data['salary_min'] = salary_min
                vac_data['salary_max'] = salary_max
                vac_data['salary_zcurrency'] = salary_zcurrency
                vac_data['link'] = link[:link.find('?')]
                vac_data['website'] = url
                vac_data['_id'] = link[22:link.find('?')]
                vaclist.append(vac_data)
                if 'hh.ru/' in link:
                    try:
                        db.vacancies.insert_one(vac_data)
                    except dke:
                        print(f"Вакансия с id = {vac_data['_id']} уже в базе.")
            print(f'Обработана {params["page"]+1}-я страница вакансий')
            params['page'] += 1
        else:
            break
vacname = input("Название желаемой позиции:\n")
pages = input("Сколько страниц поиска обработать?\n")
params = {'text' : vacname,
          'page': 0}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
vaclist = []
write_vacs(vacname,pages)