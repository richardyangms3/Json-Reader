import json
from collections import Counter, defaultdict
from datetime import datetime as dt
from datetime import timedelta
data_path = 'trainings.txt'
with open(data_path) as f:
    data = json.loads(f.read())
'''
{'name': 'Paxton Foley', 'completions': [{'name': 'Understanding Biosafety', 'timestamp': '3/23/2022', 'expires': None}]}
'''
def data_preprocess():
    hold = []
    global data
    for d in data:
        record = defaultdict(list)
        for completion in d['completions']:
            timestamp = dt.strptime(completion['timestamp'], "%m/%d/%Y")
            if completion['name'] in record:
                if timestamp > record[completion['name']][0]:
                    record[completion['name']][0] = timestamp
                    record[completion['name']][1] = completion
            else:
                record[completion['name']].append(timestamp)
                record[completion['name']].append(completion)
        filtered_result = {}
        filtered_result['name'] = d['name']
        filtered_result['completions'] = []
        for r in record.values():
            filtered_result['completions'].append(r[1])
        hold.append(filtered_result)
    data = hold
data_preprocess()

def completion_count():
    c = Counter()
    # key: training, value: count
    for d in data:
        for completion in d['completions']:
            c[completion['name']]+=1
    #print(c)
    with open('task1.json', 'w+') as f:
        res = json.dumps(c, indent=4)
        f.write(res)

completion_count()

def  completed_training_specified_fiscal_year(Trainings = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"], Fiscal_Year = 2024):
    target_training = set(Trainings)
    training2people = defaultdict(list)
    time_lowerbound = dt.strptime('7/1/'+str(Fiscal_Year-1), "%m/%d/%Y")
    time_upperbound = dt.strptime('6/30/'+str(Fiscal_Year), "%m/%d/%Y")

    for d in data:
        for completion in d['completions']:
            completion_time = dt.strptime(completion['timestamp'], "%m/%d/%Y")
            if time_lowerbound<=completion_time<=time_upperbound and completion['name'] in target_training:
                training2people[completion['name']].append(d['name'])
    #print(training2people)
    with open('task2.json', 'w+') as f:
        res = json.dumps(training2people, indent=4)
        f.write(res)

completed_training_specified_fiscal_year()

def completed_training_expired(date = '10/1/2023'):
    expire_date = dt.strptime(date, "%m/%d/%Y")
    person2training = defaultdict(list)
    for d in data:
        for completion in d['completions']:
            completion_time = dt.strptime(completion['timestamp'], "%m/%d/%Y")
            if completion_time > expire_date:
                dic = {}
                dic['training'] = completion['name']
                dic['expired or expires soon'] = 'expired'
                person2training[d['name']].append(dic)
            if completion_time+timedelta(days=30) > expire_date:
                dic = {}
                dic['training'] = completion['name']
                dic['expired or expires soon'] = 'expires soon'
                person2training[d['name']].append(dic)
    #print(person2training)
    with open('task3.json', 'w+') as f:
        res = json.dumps(person2training, indent=4)
        f.write(res)

completed_training_expired()