from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class AddBookForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    end_date = IntegerField('Дата написания', validators=[DataRequired()])
    bought = BooleanField('Книга есть в наличии?')
    author = StringField('Автор', validators=[DataRequired()])

    submit = SubmitField('Отправить')
