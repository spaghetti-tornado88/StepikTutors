# Не уверен, что все правильно оформлено с импортами
import json
from flask import render_template, request
from sqlalchemy import func
from models import Tutor, Request, Booking, app, db
from forms import *

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.secret_key = 'you-shall-not-pass'


goals = {"travel": "для путешествий",
         "study": "для учебы",
         "work": "для работы",
         "relocate": "для переезда"}


@app.route('/')
def main_page():
    # returns page with three randomly choosen tutors from database
    return render_template('index.html', tutors=db.session.query(Tutor).order_by(func.random()).limit(3))


@app.route('/all_tutors')
def all_tutors():
    # returns page with all tutors from database sorted by rating
    return render_template('index.html', tutors=db.session.query(Tutor).order_by(Tutor.rating.desc()).all())


@app.route('/goal/<goal_tag>')
def goal_page(goal_tag):
    # returns page with all tutors sorted by goals
    return render_template('goal.html', tutors=db.session.query(Tutor).filter(Tutor.goals.contains(goal_tag)),
                           goal=goals.get(goal_tag))


@app.route('/profile/<int:tutor_id>')
def profile_page(tutor_id):
    tutor = db.session.query(Tutor).get_or_404(tutor_id)
    # returns page of tutor's profile
    # json.loads(tutor.free) to draw table with tutor's schedule
    return render_template('profile.html', tutor=tutor, free=json.loads(tutor.free))

# I'm not sure: maybe it well be better ti unite this two routes
# /booking and /booking_done as /booking and just render two pages depending on the result?
@app.route('/booking/<int:tutor_id>/<day>/<time>', methods=['GET', 'POST'])
def booking_page(tutor_id, day, time):
    form = BookingForm()
    if request.method == 'POST' and form.validate():
        return booking_done_page()
    return render_template('booking.html', tutor=db.session.query(Tutor).get(tutor_id),
                           day=day, time=time, tutor_id=tutor_id, form=form)


@app.route('/booking_done', methods=['GET', 'POST'])
def booking_done_page():
    # !!!spagheti code!!!
    form = request.form
    tutor = db.session.query(Tutor).get(int(request.form.get('tutor_id')))
    day = request.form.get('day')
    time = request.form.get('time')
    booking_obj = Booking(tutor=tutor, day=day, time=time, name=request.form.get('name'), phone=request.form.get('phone'))
    db.session.add(booking_obj)
    # transfer json str in dict and change value for day&time sell in schedule
    json_daytime = json.loads(tutor.free)
    json_daytime[request.form.get('day')][request.form.get('time')] = False
    tutor.free = json.dumps(json_daytime)
    db.session.commit()
    return render_template('booking_done.html', tutor=tutor, form=form)


@app.route('/request/')
def request_page():
    form = RequestForm()
    return render_template('request.html', form=form)


@app.route('/request_done/', methods=['POST'])
def request_done_page():
    db.session.add(Request(goal=request.form.get('goal'), time=request.form.get('time'),
                   name=request.form.get('name'), phone=request.form.get('phone')))
    db.session.commit()
    return render_template('request_done.html', form=request.form)


app.run()