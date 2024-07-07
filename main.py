import asyncio
import threading
import time

import uvicorn
from fastapi import FastAPI, Request
from uvicorn.config import LOGGING_CONFIG

app = FastAPI()

LOGGING_CONFIG["formatters"]["access"][
    "fmt"
] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'


@app.middleware("http")
async def cal_time(req: Request, call_next):
    start = time.time()
    response = await call_next(req)
    process_time = time.time() - start
    print(f"接口{req.url.path} use {process_time} sec.")
    return response


@app.get("/test1")
def test1():
    print(threading.current_thread(), "test1")
    return "test1"


@app.get("/test3")
def test3():
    print(threading.current_thread(), "test3")
    time.sleep(5)
    return "test3"


# will block other api, can't use async in non await test2 test1, will block test1
@app.get("/test2")
async def test2():
    print(threading.current_thread(), "test2")
    time.sleep(5)
    return "test2"


@app.get("/test4")
async def test4():
    print(threading.current_thread(), "test4")
    await asyncio.sleep(5)
    return "test4"


if __name__ == "__main__":

    # uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    uvicorn.run("__main__:app", host="127.0.0.1", port=8000, reload=True)
