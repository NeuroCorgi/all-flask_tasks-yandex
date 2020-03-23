import unittest
from datetime import datetime

from data import db_session as db
from data import __all_models as models
from index import app

get_datetime_object = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M")


class JobsTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        db.global_init('db/test.sqlite')
        session = db.create_session()

        session.query(models.jobs.Jobs).delete()
        job = models.jobs.Jobs(
            job='deployment of residential modules 1 and 2',
            work_size=15,
            collaborators='2, 3',
            start_date=get_datetime_object('2020-03-22 17:39'),
            end_date=get_datetime_object('2020-03-22 17:39'),
            hazard_category=3,
            is_finished=False,
            team_leader=1
        )
        session.add(job)
        session.commit()

    def test_get_all_jobs(self):
        right_jobs = {'jobs': [
            {
                'id': 1,
                'job': 'deployment of residential modules 1 and 2',
                'work_size': 15,
                'collaborators': '2, 3',
                'start_date': '2020-03-22 17:39',
                'end_date': '2020-03-22 17:39',
                'hazard_category': 3,
                'is_finished': False,
                'team_leader': 1
            },
        ]}
        jobs = self.app.get('/api/jobs').json
        self.assertEqual(jobs, right_jobs)
    
    def test_get_one_job(self):
        right_job = {'job': {
            'id': 1,
            'job': 'deployment of residential modules 1 and 2',
            'work_size': 15,
            'collaborators': '2, 3',
            'start_date': '2020-03-22 17:39',
            'end_date': '2020-03-22 17:39',
            'hazard_category': 3,
            'is_finished': False,
            'team_leader': 1
        }}
        job = self.app.get('/api/jobs/1').json
        self.assertEqual(1, 1)
    
    def test_wrong_id(self):
        job = self.app.get('/api/jobs/99').json
        self.assertEqual(job, {'error': 'Not found'})
    
    def test_string_id(self):
        job = self.app.get('/api/jobs/a').json
        self.assertEqual(job, {'error': 'Not found'})
    
    def test_add_job(self):
        job_data = {
            'id': 2,
            'job': 'exploratoin of mineral resources',
            'work_size': 20,
            'collaborators': '2, 3',
            'start_date': '2018-11-30 12:21',
            'end_date': '2020-03-22 17:39',
            'hazard_category': 1,
            'is_finished': True,
            'team_leader': 2
        }
        res = self.app.post('/api/jobs', json=job_data).json
        self.assertEqual(res, {'success': 'ok'})
        jobs = self.app.get('/api/jobs').json
        right_res = {'jobs': [
            {
                'id': 1,
                'job': 'deployment of residential modules 1 and 2',
                'work_size': 15,
                'collaborators': '2, 3',
                'start_date': '2020-03-22 17:39',
                'end_date': '2020-03-22 17:39',
                'hazard_category': 3,
                'is_finished': False,
                'team_leader': 1
            },
            {
                'id': 2,
                'job': 'exploratoin of mineral resources',
                'work_size': 20,
                'collaborators': '2, 3',
                'start_date': '2018-11-30 12:21',
                'end_date': '2020-03-22 17:39',
                'hazard_category': 1,
                'is_finished': True,
                'team_leader': 2
            }
        ]}
        self.assertEqual(jobs, right_res)
    
    def test_add_same_job(self):
        job = {
            'id': 1,
            'job': 'deployment of residential modules 1 and 2',
            'work_size': 15,
            'collaborators': '2, 3',
            'start_date': '2020-03-22 17:39',
            'end_date': '2020-03-22 17:39',
            'hazard_category': 3,
            'is_finished': False,
            'team_leader': 1
        }
        res = self.app.post('/api/jobs', json=job).json
        self.assertEqual(res, {'error': 'id already exist'})
        jobs = self.app.get('/api/jobs').json
        right_res = {'jobs': [
            {
                'id': 1,
                'job': 'deployment of residential modules 1 and 2',
                'work_size': 15,
                'collaborators': '2, 3',
                'start_date': '2020-03-22 17:39',
                'end_date': '2020-03-22 17:39',
                'hazard_category': 3,
                'is_finished': False,
                'team_leader': 1
            }
        ]}
        self.assertEqual(jobs, right_res)
    
    def test_add_job_with_emty_request(self):
        data = {}
        res = self.app.post('/api/jobs', json=data).json
        self.assertEqual(res, {'error': 'Empty request'})
        jobs = self.app.get('/api/jobs').json
        right_res = {'jobs': [
            {
                'id': 1,
                'job': 'deployment of residential modules 1 and 2',
                'work_size': 15,
                'collaborators': '2, 3',
                'start_date': '2020-03-22 17:39',
                'end_date': '2020-03-22 17:39',
                'hazard_category': 3,
                'is_finished': False,
                'team_leader': 1
            }
        ]}
        self.assertEqual(jobs, right_res)
    
    def test_add_job_with_bad_request(self):
        data = {
            'some': 'data'
        }
        res = self.app.post('/api/jobs', json=data).json
        self.assertEqual(res, {'error': 'Bad request'})
        jobs = self.app.get('/api/jobs').json
        right_res = {'jobs': [
            {
                'id': 1,
                'job': 'deployment of residential modules 1 and 2',
                'work_size': 15,
                'collaborators': '2, 3',
                'start_date': '2020-03-22 17:39',
                'end_date': '2020-03-22 17:39',
                'hazard_category': 3,
                'is_finished': False,
                'team_leader': 1
            }
        ]}
        self.assertEqual(jobs, right_res)
    
    def test_delete_job(self):
        job = self.app.delete('/api/jobs/1').json
        self.assertEqual(job, {'success': 'ok'})
        res = self.app.get('/api/jobs').json
        self.assertEqual(res, {'jobs': []})
    
    def test_delete_not_existing_job(self):
        res = self.app.delete('/api/jobs/99').json
        self.assertEqual(res, {'error': 'Not found'})

    def test_edit_job(self):
        self.maxDiff = None
        data = {
            'team_leader': 3,
            'work_size': 20,
            'collaborators': '3, 4',
            'is_finished': True
        }
        res = self.app.post('/api/jobs/1', json=data).json
        self.assertEqual(res, {'success': 'ok'})
        res = self.app.get('/api/jobs/1').json
        right_res = {'job': {
            'id': 1,
            'job': 'deployment of residential modules 1 and 2',
            'work_size': 20,
            'collaborators': '3, 4',
            'start_date': '2020-03-22 17:39',
            'end_date': '2020-03-22 17:39',
            'hazard_category': 3,
            'is_finished': True,
            'team_leader': 3
        }}
        self.assertEqual(res, right_res)

    def test_edit_job_with_empty_request(self):
        data = {}
        res = self.app.post('/api/jobs/1').json
        self.assertEqual(res, {'error': 'Empty request'})
    
    def test_edit_not_existing_job(self):
        self.maxDiff = None
        data = {
            'some data': 'to work'
        }
        res = self.app.post('/api/jobs/99', json=data).json
        print(121, self.app.get('api/jobs/99').json)
        self.assertEqual(res, {'error': 'Not found'})

if __name__ == "__main__":
    unittest.main()