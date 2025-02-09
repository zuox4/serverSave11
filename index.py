import json

import requests
from datetime import datetime, timedelta

from flask import Flask, jsonify,request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/submit", methods=['POST'])
def get_data():
    data = request.json['childrenData']  # Если данные отправлены в формате JSON
    data_list = []
    end_json = []
    for i in data:
        data_list.append(get_works_days(i))
    for i in data_list:
        for j in i:
            end_json.append(j)
    with open(f'{request.json['className']}.json', 'w') as json_file:
        json.dump(end_json, json_file)
    return jsonify({"status": "success", "data": data})



def data_classes():
    klasses = []
    for i in [11,25,35,72,77,80,109,116]:
        url = f'https://pass-api.1298.ru/get_info_mentor/{i}'
        data = requests.get(url).json()
        klasses.append(data)
    print(klasses)

def get_works_days(user_exit_times):
    from datetime import datetime, timedelta
    from itertools import cycle
    ch_id = user_exit_times['data'][0]
    user_exit_times = user_exit_times['data'][1:5]
    current_date = datetime.now()
    end_date = datetime(current_date.year, 6, 30)
    exit_time_cycle = cycle(user_exit_times)
    schedule = {}
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Если день с понедельника по пятницу
            schedule[current_date.strftime("%Y-%m-%d")] = next(exit_time_cycle)
        current_date += timedelta(days=1)
    data_list_out = []
    for date, exit_time in schedule.items():
        data_list_out.append({'ch_id': ch_id,'date': date,'time': exit_time})
    return data_list_out
# get_works_days(obj[0])
if __name__ == '__main__':
    app.run()