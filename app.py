from datetime import datetime
import json
import random
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
#from flask_sqlalchemy import SQLAlchemy
from models import *
from forms import *

#app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

app.secret_key = 'absolutely-secret'

#db = SQLAlchemy(app)

migrate = Migrate(app, db)


goals = {"travel": "для путешествий",
		"study": "для учебы",
		"work": "для работы",
		"relocate": "для переезда"}


@app.route('/')
def main_page():
    # days = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}
    # free_tutors = []
    # hour = datetime.now().time().hour
    # for tutor in tutors:
    #     if tutor['free'].get(days[datetime.now().weekday()]).get(str(hour - hour % 2)+':00'):
    #         free_tutors.append(tutor)
    # return render_template('index.html', tutors=random.sample(free_tutors, 3))
    return render_template('index.html', tutors=db.session.query(Tutor).order_by(Tutor.rating.desc()).limit(3))


@app.route('/all_tutors')
def all_tutors():
    return render_template('index.html', tutors=db.session.query(Tutor).order_by(Tutor.rating.desc()).all())


@app.route('/goal/<goal_tag>')
def goal_page(goal_tag):
    return render_template('goal.html', tutors=db.session.query(Tutor).filter(Tutor.goals.contains(goal_tag)), goal=goals.get(goal_tag))


@app.route('/profile/<int:tutor_id>')
def profile_page(tutor_id):
    tutor = db.session.query(Tutor).get_or_404(tutor_id)
    return render_template('profile.html', tutor=tutor, free=json.loads(tutor.free))


@app.route('/booking/<int:tutor_id>/<day>/<time>', methods=['GET', 'POST'])
def booking_page(tutor_id, day, time):
    form = BookingForm()
    if form.validate_on_submit():
        print('1')
        return render_template('booking.html', tutor=db.session.query(Tutor).get(tutor_id),
                               day=day, time=time, tutor_id=tutor_id, form=form)
    print('2')
    return redirect(url_for('booking_page', day=day, time=time, tutor_id=tutor_id))




@app.route('/booking_done', methods=['POST'])
def booking_done_page():
    form = request.form
    tutor = db.session.query(Tutor).get(int(request.form.get('tutor_id')))
    day = request.form.get('day')
    time = request.form.get('time')
    booking_obj = Booking(tutor=tutor, day=day, time=time, name=request.form.get('name'), phone=request.form.get('phone'))
    db.session.add(booking_obj)
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