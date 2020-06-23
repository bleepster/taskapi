import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
allowed_commands = os.getenv("ALLOWED_COMMANDS")


class BaseConfig(object):
    WTF_CSRF_ENABLED = True
    ALLOWED_COMMANDS = allowed_commands.split(",")


class DevelopmentConfig(BaseConfig):
    WTF_CSRF_ENABLED = False
