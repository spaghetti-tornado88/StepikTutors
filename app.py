from flask import Flask, render_template, request, session
from datetime import datetime
import json
import random


app = Flask(__name__)
app.secret_key = 'I have no idea'

with open('data.json', 'r', encoding='utf-8') as file:
    data = file.read()

data = json.loads(data)

goals = data['goals']
tutors = data['tutors']


@app.route('/')
def main_page():
    days = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}
    free_tutors = []
    hour = datetime.now().time().hour
    for tutor in tutors:
        if tutor['free'].get(days[datetime.now().weekday()]).get(str(hour - hour % 2)+':00'):
            free_tutors.append(tutor)
    return render_template('index.html', tutors=random.sample(free_tutors, 3))


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
    return render_template('profile.html', tutor=tutor_by_id, goals=goals)


@app.route('/booking/<int:tutor_id>')
def booking_page(tutor_id):
    for tutor in tutors:
        if tutor.get('id') == tutor_id:
            tutor_by_id = tutor
            break
    # Использую сессии, хотя до конца не уверен, что всё правильно делаю, п
    # поскольку не приступал еще к следующей главе
    session['day'] = request.args.get('d')
    session['time'] = request.args.get('t')

    return render_template('booking.html', tutor=tutor_by_id, day=session['day'],
                           time=session['time'])


@app.route('/booking_done')
def booking_done_page():
    name = request.args.get('n')
    phone = request.args.get('p')
    return render_template('booking_done.html', name=name, phone=phone,
                           day=session['day'], time=session['time'])


@app.route('/request/')
def request_page():
    return render_template('request.html')


@app.route('/request_done/')
def request_done_page():
    time = request.args.get('time')
    goal = request.args.get('goal')
    print(time, goal)
    return render_template('request_done.html',
                           name=request.args.get('name'),
                           phone=request.args.get('phone'),
                           time=time, goal=goals.get(goal))


app.run()