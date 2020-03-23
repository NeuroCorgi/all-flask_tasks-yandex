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
    JobForm
)

blueprint = Blueprint('jobs_view', __name__,
                      template_folder="templates/jobs")


@blueprint.route('/jobs')
def jobs_table():
    session = db.create_session()
    jobs = session.query(models.jobs.Jobs).all()
    return render_template('jobs_table.html', current_user=current_user,
                           jobs=jobs)


@blueprint.route('/jobs/new', methods=['POST', 'GET'])
@login_required
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        session = db.create_session()
        job = models.jobs.Jobs(
            job=form.job.data,
            work_size=form.work_size.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
            team_leader=form.team_leader.data,
            hazard_category=form.hazard_category.data
        )
        session.add(job)
        session.commit()
        return redirect('/jobs')
    return render_template('new_job.html', title='New job', form=form, current_user=current_user)


@blueprint.route('/jobs/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        session = db.create_session()
        job = session.query(models.jobs.Jobs).filter(models.jobs.Jobs.id == id, 
                                                     ((models.jobs.Jobs.user == current_user) | (models.jobs.Jobs.team_leader == 1))).first()
        if job:
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.start_date.data = job.start_date
            form.end_date.data = job.end_date
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
            form.team_leader.data = job.team_leader
            form.hazard_category.data = job.hazard_category
        else:
            abort(404)
    if form.validate_on_submit():
        session = db.create_session()
        job = session.query(models.jobs.Jobs).filter(models.jobs.Jobs.id == id, 
                                                     ((models.jobs.Jobs.user == current_user) | (models.jobs.Jobs.team_leader == 1))).first()
        if job:
            job.job=form.job.data
            job.work_size=form.work_size.data
            job.start_date=form.start_date.data
            job.end_date=form.end_date.data
            job.collaborators=form.collaborators.data
            job.is_finished=form.is_finished.data
            job.team_leader=form.team_leader.data
            job.hazard_category=form.hazard_category.data
            session.commit()
            return redirect('/jobs')
        else:
            abort(404)
    return render_template('new_job.html', title='Редактирование новости', form=form)


@blueprint.route('/jobs/<int:id>/delete')
@login_required
def delete_job(id):
    session = db.create_session()
    job = session.query(models.jobs.Jobs).filter(models.jobs.Jobs.id == id,
                                                  ((models.jobs.Jobs.user == current_user) | (models.jobs.Jobs.team_leader == 1))).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect('/jobs')