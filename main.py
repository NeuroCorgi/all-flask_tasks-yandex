from datetime import datetime
from data import __all_models as models
from data import db_session as db



def add_capitan():
    user = models.users.User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.city_from = "kennedy"
    user.set_password('skottridley')
    session = db.create_session()
    session.add(user)
    session.commit()


def add_job():
    job = models.jobs.Jobs()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 15
    job.collaborators = "2, 3"
    job.start_date = datetime.now()
    job.is_finished = False
    job.hazard_category = 3
    session = db.create_session()
    session.add(job)
    session.commit()


if __name__ == '__main__':
    db.global_init('db/mars.sqlite')
    add_capitan()
    add_job()
