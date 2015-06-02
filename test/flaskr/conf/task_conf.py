from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'add-every-monday-morning': {
        'task': 'time_work.hello',
        'schedule': crontab(),
        'args': (16, 16),
    },
}