import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datein.settings")
app = Celery("datein")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'resetlikes': {
        'task': 'automatic.tasks.resetlikes',
        'schedule': crontab(hour='8, 17', minute='0')
    },
    'prepare_messages': {
        'task': 'automatic.tasks.prepare_messages',
        'schedule': crontab(hour='3', day_of_week='friday', minute='0')
    },
    'send_messages': {
        'task': 'automatic.tasks.send_messages',
        'schedule': crontab(hour='17', day_of_week='friday', minute='0')
    },
    'delete_profiles': {
        'task': 'automatic.tasks.delete_profiles',
        'schedule': crontab(hour='4', minute='0')
    },
}
