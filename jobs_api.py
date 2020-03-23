from flask import (
    Blueprint,
    jsonify,
    request,
)

from data import __all_models as  models
from data import db_session as db


blueprint = Blueprint('jobs_api', __name__,
                      template_folder='templates')


@blueprint.route('/api/jobs', methods=['GET', 'POST'])
def get_jobs():
    if request.method == 'GET':
        session = db.create_session()
        jobs = session.query(models.jobs.Jobs).all()
        return jsonify({'jobs': [job.to_dict() for job in jobs]})
    elif request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'error': 'Empty request'})
        elif not all(key in data for key in 
                 ('job', 'work_size', 'collaborators', 'start_date', 'end_date', 'hazard_category', 'is_finished', 'team_leader')):
            return jsonify({'error': 'Bad request'})
            
        session = db.create_session()
        job = models.jobs.Jobs(**data)
        session.add(job)
        session.commit()
        return jsonify({'success': 'ok'})


@blueprint.route('/api/jobs/<int:id>')
def get_one_job(id):
    session = db.create_session()
    job = session.query(models.jobs.Jobs).filter(models.jobs.Jobs.id == id).first()
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify({'job': job.to_dict()})