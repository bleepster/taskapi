import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
allowed_commands = os.getenv("ALLOWED_COMMANDS")

class BaseConfig(object):
    WTF_CSRF_ENABLED = True
    REDIS_URL = f"redis://{redis_host}:{redis_port}/0"
    QUEUES = ["default",]
    ALLOWED_COMMANDS = allowed_commands.split(",")


class DevelopmentConfig(BaseConfig):
    WTF_CSRF_ENABLED = False
