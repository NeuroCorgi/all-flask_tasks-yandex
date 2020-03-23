from sqlalchemy_serializer.serializer import (
    SerializerMixin
)

import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "departments"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.chief = kwargs['chief']
        self.members = kwargs['members']
        self.email = kwargs['email']

    user = orm.relation('User')