import functools

from redis import from_url
from rq import Queue, Connection

from .worker import work

from flask import (
    Blueprint,
    current_app,
    request,
    Response,
)

bp = Blueprint("task", __name__, url_prefix="/task")

@bp.route("/", methods=("POST",))
def run():
    if request.method == "POST":
        if not request.is_json:
            return Response({}, status=404, mimetype="application/json")
        params = request.get_json()
        if 'source' not in params or 'dest' not in params:
            return Response(status=404)
        with Connection(from_url(current_app.config["REDIS_URL"])):
            command = [current_app.config["COMMAND"], params["source"], params["dest"]]
            q = Queue()
            task = q.enqueue(work, command)
            if task is not None:
                tid = task.get_id()
                return {"id": tid}, 201
        return Response(status=404)
