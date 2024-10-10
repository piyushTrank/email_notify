from django.apps import AppConfig
# from App.scheduler import *  
# from apscheduler.schedulers.background import BackgroundScheduler

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'

    # def ready(self):
    #     scheduler = BackgroundScheduler()
    #     scheduler.add_job(alert_expire, 'cron', hour=23, minute=59)
    #     scheduler.start()
