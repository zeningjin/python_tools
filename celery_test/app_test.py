from celery import Celery

app = Celery('celery_test', include=['celery_test.tasks'])
app.config_from_object('celery_test.celeryconfig')

if __name__ == '__main__':
    app.start()