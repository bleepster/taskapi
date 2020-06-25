#!/usr/bin/env python

import sys
import argparse
import asyncio
import json

from aiohttp import ClientSession
from time import time, sleep


async def add_task(session, url, task_data):
    async with session.post(url, json=task_data) as resp:
        try:
            resp_obj = json.loads(await resp.text())
            return resp.status, resp_obj
        except json.decoder.JSONDecodeError:
            return 0, {}
    return 0, {}


async def get_task_status(session, url, task_id):
    async with session.get(url + task_id) as resp:
        try:
            resp_obj = json.loads(await resp.text())
            return resp.status, resp_obj
        except json.decoder.JSONDecodeError:
            return 0, {}
    return 0, {}


async def run(session, url, task_data):
    http_status, task_response = await add_task(session, url, task_data)
    if http_status != 201:
        print(f"Failed to create task: {http_status}")
        return False

    tid = task_response["id"]
    print(f'{tid}: running {task_data}')
    start = time()
    sleep_time = 0
    while True:
        http_status, task_status_response = await get_task_status(session, url, tid)
        if http_status != 200:
            print(f"Failed to retrieve task status for {tid}")
            return False

        t_status = task_status_response["status"]
        if task_status_response["status"] in ["queued", "started", "deferred"]:
            sleep(10/1000)
            sleep_time = round(sleep_time + 10/1000, 2)
            continue
        else:
            t_result = task_status_response["result"]
            print(f"{tid}: status({t_status}), result({t_result})")
            break
    end = round((time() - start), 2)
    print(f'{tid}: total time (~{end}s), sleep time (~{sleep_time}ms)')
    return True


async def do_runs(url):
    task_data = [
        {
            "binary": "/bin/dd",
            "options": ["if=/dev/urandom", "of=/tmp/test1.img", "bs=1024", "count=8K"],
        },
        {
            "binary": "/bin/dd",
            "options": ["if=/dev/urandom", "of=/tmp/test2.img", "bs=1024", "count=1K"],
        },
        {
            "binary": "/bin/dd",
            "options": ["if=/dev/urandom", "of=/tmp/test3.img", "bs=1024", "count=4K"],
        },
        {
            "binary": "/bin/dd",
            "options": ["if=/dev/urandom", "of=/tmp/test1.img", "bs=1024", "count=80K"],
        },
        {
            "binary": "/bin/dd",
            "options": ["if=/dev/urandom", "of=/tmp/test2.img", "bs=1024", "count=10K"],
        },
        {
            "binary": "/bin/dd",
            "options": ["if=/dev/urandom", "of=/tmp/test3.img", "bs=1024", "count=40K"],
        },
    ]
    async with ClientSession() as session:
        tasks = [asyncio.ensure_future(run(session, url, td)) for td in task_data]
        responses = await asyncio.gather(*tasks)
    return responses


def main(args):
    parser = argparse.ArgumentParser(description="Testing RQ")
    parser.add_argument("--host", required=True, help="Server hostname")
    parser.add_argument("--port", required=True, help="Server port")
    parsed_args = parser.parse_args(args)
    url = f"http://{parsed_args.host}:{parsed_args.port}/task/"

    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_runs(url))
    loop.close()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
