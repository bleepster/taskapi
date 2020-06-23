from . import create_app, make_celery

celery = make_celery(create_app())
