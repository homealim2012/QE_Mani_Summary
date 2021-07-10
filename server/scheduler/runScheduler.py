from flask_apscheduler import APScheduler

scheduler = APScheduler()

def init_scheduler(app):
    scheduler.init_app(app=app)
    scheduler.start()
    from server.scheduler import saveTaskScheduler
    print('scheduler started')
