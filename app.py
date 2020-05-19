import random
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import InputRequired

from db import *

with open('./db/goals.json', 'r') as r:
    goals = json.load(r)
    goals_choice = [(key, value) for key, value in goals.items()]

with open('./db/week.json', 'r') as r:
    week = json.load(r)

with open('./db/hours.json', 'r') as r:
    hours = json.load(r)
    hours_choice = [(key, value) for key, value in hours.items()]

with open('./db/teachers.json', 'r') as r:
    teachers = json.load(r)

app = Flask(__name__)
app.secret_key = "very_random_string"


@app.route('/')
def render_index():
    return render_template('index.html',
                           goals=goals,
                           teachers=random.sample(teachers, 6))


@app.route('/all/')
def render_all():
    return render_template('all.html',
                           goals=goals,
                           teachers=teachers)


@app.route('/goals/<goal>/')
def render_goal(goal):
    return render_template('goal.html',
                           goals=goals,
                           goal=goal,
                           teachers=teachers)


@app.route('/profiles/<id>/')
def render_profile(id):
    days = {}
    for day in week:
        days[day] = 0
        for status in teachers[int(id)]['free'][day].values():
            if status == True:
                days[day] += 1

    return render_template('profile.html',
                           goals=goals,
                           week=week,
                           id=id,
                           teacher=teachers[int(id)],
                           days=days)


class RequestForm(FlaskForm):
    name = StringField('Вас зовут', [InputRequired()])
    phone = StringField('Ваш телефон', [InputRequired()])
    goals = RadioField('Какая цель занятий?', choices=goals_choice, default=goals_choice[0][0])
    hours = RadioField('Сколько времени есть?', choices=hours_choice, default=hours_choice[0][0])


@app.route('/request/')
def render_request():
    form = RequestForm()

    return render_template('request.html',
                           form=form)


@app.route('/request_done/', methods=["GET", "POST"])
def render_request_done():
    if request.method == 'POST':
        form = RequestForm()

        goal = form.goals.data
        hour = form.hours.data
        name = form.name.data
        phone = form.phone.data

        add_request(goal, hour, name, phone)

        return render_template('request_done.html',
                               goal=goals[goal],
                               hours=hours[hour],
                               name=name,
                               phone=phone)
    else:
        return "Просто зашли посмотреть"


class BookingForm(FlaskForm):
    name = StringField('Вас зовут', [InputRequired()])
    phone = StringField('Ваш телефон', [InputRequired()])
    id = StringField('id')
    day = StringField('day')
    time = StringField('time')

@app.route('/booking/<id>/<day>/<time>/')
def render_booking(id, day, time):
    form = BookingForm()

    return render_template('booking.html',
                           week=week,
                           id=id,
                           teacher=teachers[int(id)],
                           day=day,
                           time=time,
                           form=form)


@app.route('/booking_done/', methods=["GET", "POST"])
def render_booking_done():
    if request.method == 'POST':
        form = BookingForm()

        id = form.id.data
        name = form.name.data
        phone = form.phone.data
        day = form.day.data
        time = form.time.data

        add_booking(id, day, time, name, phone)

        return render_template('booking_done.html',
                               name=name,
                               phone=phone,
                               day=week[day],
                               time=time)
    else:
        return "Просто зашли посмотреть"


if __name__ == '__main__':
    app.run()