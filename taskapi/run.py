import functools

from flask import (
    Blueprint,
    request,
    Response,
    current_app,
)

from .command import exec_command
from .extensions import celery

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

    task = exec_command.delay(command_params)

    return {"id": task.task_id}, 201


@bp.route("/<task_id>", methods=("GET",))
def get_task(task_id):
    result = celery.AsyncResult(task_id)
    if result:
        return {"id": result.task_id, "status": result.status}, 200
    return {}, 503
