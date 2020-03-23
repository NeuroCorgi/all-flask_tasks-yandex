from datetime import datetime

from flask import (
    Blueprint,
    jsonify,
    request,
)

from data import __all_models as  models
from data import db_session as db


blueprint = Blueprint('jobs_api', __name__,
                      template_folder='templates')

get_datetime_object = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M")


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    session = db.create_session()
    jobs = session.query(models.jobs.Jobs).all()
    return jsonify({'jobs': [job.to_dict() for job in jobs]})
        

@blueprint.route('/api/jobs', methods=['POST'])
def new_job():
    data = request.json
    keys = ('job', 'work_size', 'collaborators', 'start_date', 'end_date', 'hazard_category', 'is_finished', 'team_leader')
    if not data:
        return jsonify({'error': 'Empty request'})
    elif not all(key in data for key in keys):
        return jsonify({'error': 'Bad request'})

    data['start_date'] = get_datetime_object(data['start_date'])
    data['end_date'] = get_datetime_object(data['end_date'])

    session = db.create_session()
    job = models.jobs.Jobs(**data)
    same_job = session.query(models.jobs.Jobs).filter(*[getattr(models.jobs.Jobs, key, 0) == data[key] for key in keys]).first()
    if same_job:
        return jsonify({'error': 'id already exist'})

    session.add(job)
    session.commit()
    return jsonify({'success': 'ok'})


@blueprint.route('/api/jobs/<int:id>', methods=['GET'])
def get_one_job(id):
    session = db.create_session()
    job = session.query(models.jobs.Jobs).filter(models.jobs.Jobs.id == id).first()
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify({'job': job.to_dict()})


@blueprint.route('/api/jobs/<int:id>', methods=['POST'])
def edit_job(id):
    data = request.json
    if not data:
        return jsonify({'error': 'Empty request'})
    session = db.create_session()
    job = session.query(models.jobs.Jobs).filter(models.jobs.Jobs.id == id).first()
    if not job:
        return jsonify({'error': 'Not found'})
    for key, value in data.items():
        setattr(job, key, value)
    session.commit()
    return jsonify({'success': 'ok'})


@blueprint.route('/api/jobs/<int:id>', methods=['DELETE'])
def delete_job(id):
    session = db.create_session()
    job = session.query(models.jobs.Jobs).filter(models.jobs.Jobs.id == id).first()
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'ok'})