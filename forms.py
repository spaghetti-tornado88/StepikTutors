from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class BookingForm(FlaskForm):
    tutor_id = IntegerField()
    day = StringField()
    time = StringField()
    name = StringField('Вас зовут', [DataRequired(), Length(max=10)])
    phone = StringField('Ваш телефон', [DataRequired(), Length(max=10)])
    submit = SubmitField('Записаться')


class RequestForm(FlaskForm):
    goal = RadioField('goal', choices=[('travel', 'Для путешествий'),
                                       ('study', 'Для учёбы'),
                                       ('work', 'Для работы'),
                                       ('relocate', 'Для переезда')])

    time = RadioField('time', choices=[('1-2', '1-2 часа в неделю'),
                                       ('3-5', '3-5 часов в неделю'),
                                       ('5-7', '5-7 часов в неделю'),
                                       ('7-10', '7-10 часов в неделю')])

    name = StringField('Вас зовут', validators=[DataRequired()])
    phone = StringField('Ваш телефон', validators=[DataRequired()])
    submit = SubmitField('Найдите мне преподавателя')

