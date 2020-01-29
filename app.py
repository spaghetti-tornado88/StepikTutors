from flask import Flask, render_template
from datetime import datetime
import json
import requests
import random



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
    for tutor in tutors:
        print(tutor['free'])
        if tutor['free'].get(days[datetime.now().weekday()]).get(str(hour - hour % 2)+':00'):
            free_tutors.append(tutor)
    print(random.sample(free_tutors, 3))
    return render_template('index.html', tutors = random.sample(free_tutors, 3))


@app.route('/all_tutors')
def all_tutors():
    return render_template('index.html', tutors=tutors)


@app.route('/goal/<goal_tag>')
def goal_page(goal_tag):
    tutors_by_goal = []
    for tutor in tutors:
        if goal_tag in tutor['goals']:
            tutors_by_goal.append(tutor)
    return render_template('goal.html', goal=goals.get(goal_tag), tutors=tutors_by_goal)


@app.route('/profile/<int:tutor_id>')
def profile_page(tutor_id):
    for tutor in tutors:
        if tutor.get('id') == tutor_id:
            tutor_by_id = tutor
            break
    return render_template('profile.html', tutor = tutor_by_id)

app.run()