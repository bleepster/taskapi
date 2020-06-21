import os

basedir = os.path.abspath(os.path.dirname(__file__))
redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")

class BaseConfig(object):
    WTF_CSRF_ENABLED = True
    REDIS_URL = f'redis://{redis_host}:{redis_port}/0'
    QUEUES = ["default"]

class DevelopmentConfig(BaseConfig):
    WTF_CSRF_ENABLED = False
