from flask import (
    render_template,
    redirect,
    Blueprint
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from index import login_manager

from data import __all_models as models
from data import db_session as db

from forms import (
    RegisterForm,
    LoginForm,
)

blueprint = Blueprint('auth_api', __name__,
                      template_folder='templates/auth')


@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', current_user=current_user,
                                   form=form,
                                   message="Пароли не совпадают")
        session = db.create_session()
        if session.query(models.users.User).filter(models.users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', current_user=current_user,
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = models.users.User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, current_user=current_user)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db.create_session()
        user = session.query(models.users.User).filter(models.users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', current_user=current_user,
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, current_user=current_user)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect('/jobs')