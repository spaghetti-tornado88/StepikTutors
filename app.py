from flask import Flask, render_template, request, session
from datetime import datetime
import json
import random


app = Flask(__name__)

with open('data.json', 'r', encoding='utf-8') as file:
    data = file.read()

data = json.loads(data)

goals = data['goals']
tutors = data['tutors']


def findTutor(tutors_list, tutor_id):
    for tutor in tutors_list:
        if tutor.get('id') == tutor_id:
            return tutor


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
    return render_template('profile.html', tutor=findTutor(tutors, tutor_id), goals=goals)


@app.route('/booking/<int:tutor_id>/<day>/<time>')
def booking_page(tutor_id, day, time):
    return render_template('booking.html', tutor=findTutor(tutors, tutor_id),
                           day=day, time=time)


@app.route('/booking_done', methods=['POST'])
def booking_done_page():
    with open('booking.json', 'a') as booking_file:
        booking_file.write(json.dumps(request.form))
        booking_file.write('\n')
    return render_template('booking_done.html', tutor=findTutor(tutors, int(request.form.get('c_tutor'))),
                           booking_form=request.form)


@app.route('/request/')
def request_page():
    return render_template('request.html')


@app.route('/request_done/', methods=['POST'])
def request_done_page():
    with open('request.json', 'a') as request_file:
        request_file.write(json.dumps(request.form))
        request_file.write('\n')
    return render_template('request_done.html', request_form=request.form)


app.run()