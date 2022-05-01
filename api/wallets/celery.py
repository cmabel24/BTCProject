from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# setting the Django settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
app = Celery("wallet")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Looks up for task modules in Django applications and loades them
app.autodiscover_tasks()
