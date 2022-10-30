from apscheduler.schedulers.background import BackgroundScheduler


mail_scheduler = BackgroundScheduler()
#mail_scheduler.add_job(
#    id='mail distribution',
#    func=lambda: print('123'),
#    trigger='interval',
#    seconds = 5,
#)