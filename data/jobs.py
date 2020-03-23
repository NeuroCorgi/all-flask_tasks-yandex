import datetime

from sqlalchemy_serializer.serializer import (
    SerializerMixin
)

import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    hazard_category = sqlalchemy.Column(sqlalchemy.Integer, default=3)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    def __init__(self, **kwargs):
        if kwargs:
            self.job = kwargs['job']
            self.work_size = kwargs['work_size']
            self.collaborators = kwargs['collaborators']
            self.start_date = kwargs['start_date']
            self.end_date = kwargs['end_date']
            self.is_finished = kwargs['is_finished']
            self.team_leader = kwargs['team_leader']
            self.hazard_category = kwargs['hazard_category']

    def __repr__(self):
        return f'<Job> {self.job}'
    
    def to_dict(self):
        return super().to_dict(only=('id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'hazard_category', 'is_finished', 'team_leader'))
