import functools

from redis import from_url
from rq import Queue, Connection

from .command import exec_command

from flask import (
    Blueprint,
    current_app,
    request,
    Response,
)

bp = Blueprint("task", __name__, url_prefix="/task")


@bp.route("/", methods=("POST",))
def post_task():
    if not request.is_json:
        return {}, 400
    command = request.get_json()
    binary = command.get("binary")
    if not binary or binary not in current_app.config["ALLOWED_COMMANDS"]:
        return {}, 400
    options = command.get("options")
    command_params = [binary]
    if options:
        command_params += options
    with Connection(from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.enqueue(exec_command, command_params)
        if task is not None:
            tid = task.get_id()
            return {"id": tid}, 201
    return {}, 503


@bp.route("/<task_id>", methods=("GET",))
def get_task(task_id):
    with Connection(from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.fetch_job(task_id)
        if task is not None:
            tid = task.get_id()
            status = task.get_status()
            return {"id": tid, "status": status}, 200
        else:
            return {}, 404
    return {}, 503
