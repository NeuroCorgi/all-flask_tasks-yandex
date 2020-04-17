from datetime import datetime

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
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    city_from = sqlalchemy.Column(sqlalchemy.String)

    jobs = orm.relation('Jobs', back_populates='user')
    departments = orm.relationship('Department', back_populates='user')

    def __init__(self, 
                 surname: str,
                 name: str,
                 email: str,
                 age: int,
                 position: str,
                 speciality: str,
                 address: str,
                 city_from: str,
                 password: str,
                 modifed_date: datetime="",):
        self.email = email

        self.surname = surname
        self.name = name

        self.age = age

        self.position = position
        self.speciality = speciality

        self.address = address
        self.city_from = city_from

        self.set_password(password)
        
        if modifed_date:
            self.modifed_date = modifed_date


    def __repr__(self):
        return f"<User> {self.surname} {self.name}"
    
    def to_dict(self):
        return super().to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'modifed_date', 'city_from'))
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
