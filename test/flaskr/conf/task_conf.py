from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'add-every-monday-morning': {
        'task': 'time_work.hello',
        'schedule': crontab(minute='50,51,52'),
        'args': (16, 16),
    },
}