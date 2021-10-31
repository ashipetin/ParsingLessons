from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['testdb']
vacancies = db.vacancie


def getvacs(x):
     a = db.vacancies.find({'salary_min': {'$gt': x},'salary_max': {'$gt': x}, 'salary_zcurrency': 'руб.'})
     for vac in a:
         print(vac)
salary = int(input('Выводим вакансии с зарплатой, превышающей (в рублях):\n'))
vacs_sal_gt = getvacs(salary)
print(vacs_sal_gt)
