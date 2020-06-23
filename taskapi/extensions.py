import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_host = f"redis://{redis_host}:{redis_port}"

celery = Celery("taskapi", backend=redis_host, broker=redis_host)
