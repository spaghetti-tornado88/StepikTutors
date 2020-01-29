from flask import Flask, render_template
import json
import requests
from datetime import datetime


days = {0: "mon", 1: "tue", 2: "wed",3: "thu", 4: "fri", 5: "sat", 6: "sun"}
app = Flask(__name__)

with open('data.json', 'r', encoding='utf-8') as file:
    data = file.read()

data = json.loads(data)

goals = data['goals']
tutors = data['tutors']


@app.route('/')
def main_page():
    free_tutors = []
    print(days[datetime.now().weekday()])
    print(datetime.now().time().hour, datetime.now().minute)
    hour = datetime.now().time().hour
    if hour % 2:
        hour -= 1
    for tutor in tutors:
        print(tutor['free'])
        if tutor['free'][days[datetime.now().weekday()]][str(hour)+':00']:
            free_tutors.append(tutor)
    print(free_tutors)
    return render_template('index.html')


@app.route('/all_tutors')

def all_tutors():
    return render_template('index.html', tutors=tutors)

app.run()