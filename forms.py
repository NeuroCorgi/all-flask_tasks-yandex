from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    IntegerField,
    DateField,
)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repear passowrd', validators=[DataRequired()])

    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])

    age = IntegerField('Age', validators=[DataRequired()])

    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Spiciality', validators=[DataRequired()])

    address = StringField("Address", validators=[DataRequired()])

    submit = SubmitField('Register')


class JobForm(FlaskForm):

    job = StringField('Job', validators=[DataRequired()])
    team_leader = StringField('Team leader id')

    work_size = IntegerField('Work size', validators=[DataRequired()])

    collaborators = StringField('Collaborators')

    start_date = DateField('Start date')
    end_date = DateField('End date')

    hazard_category = IntegerField('Hazard category', validators=[DataRequired()])

    is_finished = BooleanField('Is finished')

    submit = SubmitField("Submit")


class DepartmentForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])

    chief = IntegerField('Chief id', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    
    email = StringField('Email', validators=[DataRequired()])

    submit = SubmitField("Submit")
