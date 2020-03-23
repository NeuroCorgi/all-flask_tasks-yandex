from flask import (
    render_template,
    redirect,
    abort
)
from flask_login import (
    current_user,
    login_required,
)

from index import app

from data import __all_models as models
from data import db_session as db


@app.route('/users/<int:id>')
def user_home(id):
    session = db.create_session()
    user = session.query(models.users.User).filter(models.users.User.id == id).first()
    if not user:
        redirect('/login')
    if current_user != current_user:
        abort(404)
    jobs = user.jobs
    return render_template('user_home.html', title=user.surname,
                           user=user, jobs=jobs)