from flask.cli import FlaskGroup
from redis import from_url
from rq import Connection, Worker

from taskapi import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("workers")
def run_workers():
    with Connection(from_url(app.config["REDIS_URL"])):
        worker = Worker(app.config["QUEUES"])
        worker.work()

if __name__ == "__main__":
    cli()
