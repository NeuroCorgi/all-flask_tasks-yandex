from flask import (
    Blueprint,
    render_template,
    redirect,
    abort,
    request
)
from flask_login import (
    current_user,
    login_required,
)

from data import __all_models as  models
from data import db_session as db
from forms import (
    DepartmentForm
)

blueprint = Blueprint('departments_api', __name__,
                      template_folder="templates/departments")


@blueprint.route('/departments')
def deps_table():
    session = db.create_session()
    deps = session.query(models.departments.Department).all()
    return render_template('deps_table.html', current_user=current_user,
                           deps=deps)


@blueprint.route('/departments/new', methods=['POST', 'GET'])
def new_dep():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = db.create_session()
        dep = models.departments.Department(
            title=form.title.data,
            members=form.members.data,
            chief=form.chief.data,
            email=form.email.data
        )
        session.add(dep)
        session.commit()
        return redirect('/departments')
    return render_template('new_dep.html', title='New departments', form=form, current_user=current_user)


@blueprint.route('/departments/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_dep(id):
    form = DepartmentForm()
    if request.method == "GET":
        session = db.create_session()
        dep = session.query(models.departments.Dep).filter(models.departments.Department.id == id, 
                                                     ((models.departments.Department.user == current_user) | (current_user.id == 1))).first()
        if dep:
            form.title.data = dep.title
            form.members.data = dep.members
            form.chief.data = dep.chief
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db.create_session()
        job = session.query(models.jobs.Jobs).filter(models.jobs.Jobs.id == id, 
                                                     ((models.jobs.Jobs.user == current_user) | (models.jobs.Jobs.team_leader == 1))).first()
        if job:
            title=form.title.data
            members=form.members.data
            chief=form.chief.data
            emai=form.email.data
            session.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('new_dep.html', title='Редактирование новости', form=form)


@blueprint.route('/departments/<int:id>/delete')
@login_required
def delete_dep(id):
    session = db.create_session()
    dep = session.query(models.departments.Department).filter(models.departments.Department.id == id,
                                                  ((models.departments.Department.user == current_user) | (models.departments.Department.chief == 1))).first()
    if dep:
        session.delete(dep)
        session.commit()
    else:
        abort(404)
    return redirect('/departments')
