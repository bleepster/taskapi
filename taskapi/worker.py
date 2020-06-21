from subprocess import (
    CalledProcessError,
    run,
    TimeoutExpired,
)


def do_work(command):
    try:
        run(command, timeout=15)
    except TimeoutExpired:
        return False
    except CalledProcessError:
        return False
    return True


def work(command=None):
    if command is not None and isinstance(command, list) and len(command) > 0:
        return do_work(command)
