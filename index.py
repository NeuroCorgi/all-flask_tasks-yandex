from uuid import uuid4
from datetime import timedelta

from flask import (
    Flask,
    render_template,
    redirect,
    make_response,
    jsonify
)
from flask_login import (
    LoginManager,
    current_user,
)
from flask_restful import Api

from data import __all_models as models
from data import db_session as db

from forms import (
    RegisterForm,
    LoginForm,
)

app = Flask(__name__)

api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)
    
import auth

import jobs_view
import departments_view
import users_view

import users_resource
import jobs_resource


@login_manager.user_loader
def load_user(user_id):
    session = db.create_session()
    return session.query(models.users.User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
@app.route('/index')
def home():
    return redirect('/jobs')
    return render_template('base.html', current_user=current_user,
                           title='Mars')


app.register_blueprint(auth.blueprint)

# Views
app.register_blueprint(jobs_view.blueprint)
app.register_blueprint(departments_view.blueprint)
app.register_blueprint(users_view.blueprint)

# Restful api
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')

api.add_resource(jobs_resource.JobsListResource, '/api/jobs')
api.add_resource(jobs_resource.JobsResource, '/api/jobs/<int:job_id>')


def main():
    app.config['SECRET_KEY'] = str(uuid4())
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
    app.config['DATABASE_NAME'] = 'db/mars.sqlite'

    db.global_init(app.config['DATABASE_NAME'])

    app.run()


if __name__ == '__main__':
    main()