from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gettingstarted.settings')

from django.conf import settings  # noqa

app = Celery('proj')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
#app.config_from_object('django.conf:settings')

# if 'REDIS_URL' exists, then it's heroku
if os.environ.has_key('REDIS_URL'):
	redis_url = os.environ['REDIS_URL']
else:
	redis_url = 'redis://localhost:6379/0'
print(redis_url)
app.conf.update(BROKER_URL=redis_url, CELERY_RESULT_BACKEND=redis_url)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))

@app.task
def add(x, y):
	print("add task")
	return x + y