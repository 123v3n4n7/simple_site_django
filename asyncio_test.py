import asyncio
import time
import requests
import aiohttp
from collections import namedtuple
from aiohttp import client_exceptions
import argparse
import random

def_timeout = 0.1

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
            Service('ip-api', 'http://ip-api.com/json', 'query'),
            #Service('broken', 'http://ipBBBapi.com/json', 'query')
            )


async def fetch_async(session, service):
    print('ip from {}'.format(service.name))
    try:
        await asyncio.sleep(random.randint(1, 3) * 0.1)
        async with session.get(service.url) as response:
                json_resp = await response.json()
                ip = json_resp[service.ip_attr]
                print(ip)
    except client_exceptions.ClientConnectionError:
        return '{} is broken'.format(service.name)
    return ip


async def asynchronous(timeout):
    response = {
        "message": "Result from asynchronus",
        "ip": "not available"
    }
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_async(session, service) for service in SERVICES]
        done, pending = await asyncio.wait(tasks, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        for task in done:
            response["ip"] = (task.result())
    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timeout', help='Timeout to use, defaults to {}'.format(def_timeout),
                        default=def_timeout, type=float)
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asynchronous(args.timeout))
    loop.close()



#
# async def fetch_async(session, pid):
#     async with session.get('http://www.python.org') as response:
#         datetime = response.headers.get('Date')
#         #text = await response.text()
#         print(datetime, pid)
#     return datetime
#
#
# async def asynchronous():
#     async with aiohttp.ClientSession() as session:
#         tasks = [asyncio.ensure_future(fetch_async(session, i)) for i in range(1, max_clients+1)]
#         await  asyncio.wait(tasks)
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asynchronous())
#     loop.close()

# start = time.time()
#
#
# def tic():
#     answer = requests.get('http://www.python.org')
#     return '{}'.format(answer.text)
#
#
# async def gr1():
#     print('gr1 started work: {}'.format(tic()))
#     await asyncio.sleep(0)
#     print('gr1 ended work: {}'.format(tic()))
#
#
# async def gr2():
#     print('gr2 started work: {}'.format(tic()))
#     await asyncio.sleep(0)
#     print('gr2 ended work: {}'.format(tic()))
#
#
# async def gr3():
#     print('Some work gr3')
#     await asyncio.sleep(1)
#     print('done!!!')
#
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     tasks = [
#         loop.create_task(gr1()),
#         loop.create_task(gr2()),
#         loop.create_task(gr3()),
#     ]
#     loop.run_until_complete(asyncio.wait(tasks))
#     loop.close()

# async def foo():
#     print("Запуск foo")
#     await asyncio.sleep(10)
#     print("Переключение на foo")
#
#
# async def bar():
#     print("Запуск bar")
#     await asyncio.sleep(5)
#     print("Переключение на bar")
#
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     task1 = loop.create_task(foo())
#     task2 = loop.create_task(bar())
#     tasks = [task1, task2]
#     loop.run_until_complete(asyncio.wait(tasks))
#     loop.close()
#