import datetime

from sqlalchemy_serializer.serializer import (
    SerializerMixin
)

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

from flask_login.mixins import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    speciality = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    city_from = sqlalchemy.Column(sqlalchemy.String)

    jobs = orm.relation('Jobs', back_populates='user')
    departments = orm.relationship('Department', back_populates='user')

    def __init__(self, **kwargs):
        if kwargs:
            self.email = kwargs['email']

            self.surname = kwargs['surname']
            self.name = kwargs['name']

            self.age = kwargs['age']

            self.position = kwargs['position']
            self.speciality = kwargs['speciality']

            self.address = kwargs['address']


    def __repr__(self):
        return f"<User> {self.surname} {self.name}"
    
    def to_dict(self):
        return super().to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'modifed_date', 'city_from'))
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
