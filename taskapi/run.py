import functools

from flask import (
    Blueprint,
    request,
    Response,
)

bp = Blueprint("run", __name__, url_prefix="/run")


@bp.route("/", methods=("PUT",))
def run():
    if request.method == "PUT":
        return Response({}, status=204, mimetype="application/json")
