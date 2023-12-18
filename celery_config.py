from celery import Celery

app = Celery(
    'main',
    broker='pyamqp://user:password@rabbitmq//',
    backend='rpc://',
    include=['auth.tasks']
)


app.conf.update(
    result_expires=3600,
)