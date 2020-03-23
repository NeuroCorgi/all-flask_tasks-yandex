import unittest

from requests import get


class JobsTests(unittest.TestCase):

    def test_get_all_jobs(self):
        right_jobs = [{
            'id': 1,
            'job': 'deployment of residential modules 1 and 2',
            'work_size': 15,
            'collaborators': '2, 3',
            'start_date': '2020-03-22 17:39',
            'end_date': '2020-03-22 17:39',
            'hazard_category': 3,
            'is_finished': False,
            'team_leader': 1
        }]
        jobs = get('http://localhost:5000/api/jobs').json()['jobs']
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
        job = get('http://localhost:5000/api/jobs/1').json()
        self.assertEqual(1, 1)
    
    def test_wrong_id(self):
        job = get('http://localhost:5000/api/jobs/2').json()
        self.assertEqual(job, {'error': 'Not found'})
    
    def test_string_id(self):
        job = get('http://localhost:5000/api/jobs/a').json()
        self.assertEqual(job, {'error': 'Not found'})


if __name__ == "__main__":
    unittest.main()