import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length


class BookingForm(FlaskForm):
    tutor_id = IntegerField()
    day = StringField()
    time = StringField()
    name = StringField('Вас зовут', [DataRequired(message='Введите свое имя')])
    phone = StringField('Ваш телефон', [DataRequired(message='Введите свой номер телефона'), Length(max=16)])
    submit = SubmitField('Записаться')

    def validate_phone(form, field):
        if not phonenumbers.is_valid_number(phonenumbers.parse(field.data, 'RU')):
            raise ValidationError('Введите номер телефона в правильном формате!')


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

