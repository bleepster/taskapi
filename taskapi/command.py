from .extensions import celery
from subprocess import (
    CalledProcessError,
    run,
    TimeoutExpired,
)


@celery.task()
def exec_command(params=None):
    if not params:
        return False
    try:
        run(params, timeout=15)
    except TimeoutExpired:
        return False
    except CalledProcessError:
        return False
    return True
