import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Books(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    bought = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    def __repr__(self):
        return f'<Book> {self.book}'
