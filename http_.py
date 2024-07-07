import time

import httpx
from httpx import Response
from tqdm import tqdm

from config import HEADER, LIMIT


class Session:
    # sigleton
    _instance = None

    # cookies
    cookies = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Session, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        import pathlib
        if pathlib.Path('cookies.pkl').exists():
            self._load_from_local()

    def set_cookies(self, cookies: dict):
        self.cookies = cookies
        self._write_to_local()

    def _write_to_local(self):
        import json
        with open('cookies.json', 'wb') as f:
            f.write(json.dumps(dict(self.cookies)).encode())

    def _load_from_local(self):
        import pathlib
        if not pathlib.Path('cookies.json').exists():
            return
        import json

        from httpx import Cookies
        with open('cookies.json', 'rb') as f:
            try:
                httpx_cookies = Cookies(json.loads(f.read()))
            except Exception as e:
                tqdm.write(str(e))
                return
            self.cookies = httpx_cookies


Session = Session()
Session._load_from_local()


async def get(url: str, *args, **kwargs) -> Response:
    try:
        async with LIMIT:
            async with httpx.AsyncClient(headers=HEADER,
                                         cookies=Session.cookies,
                                         follow_redirects=True,
                                         timeout=3) as client:
                time.sleep(0.25)
                resp = await client.get(url, *args, **kwargs)
                if resp.text == '{"error":{"code":"RATE_LIMIT_EXCEEDED","message":"您访问得太快啦，不如休息一会儿吧"}}':
                    tqdm.write('您访问得太快啦，不如休息一会儿吧')
                    time.sleep(3)
                if resp.status_code != 200:
                    tqdm.write(resp.text)
                return resp
    except Exception as e:
        tqdm.write(str(e))
        time.sleep(1)
        return await get(url, *args, **kwargs)


async def post(url: str, *args, **kwargs) -> Response:
    try:
        async with LIMIT:
            async with httpx.AsyncClient(headers=HEADER,
                                         cookies=Session.cookies,
                                         follow_redirects=True,
                                         timeout=3) as client:
                time.sleep(0.25)
                resp = await client.post(url, *args, **kwargs)
                if resp.text == '{"error":{"code":"RATE_LIMIT_EXCEEDED","message":"您访问得太快啦，不如休息一会儿吧"}}':
                    tqdm.write('您访问得太快啦，不如休息一会儿吧')
                    time.sleep(3)
                if resp.status_code != 200:
                    tqdm.write(resp.text)
                return resp
    except Exception as e:
        tqdm.write(str(e))
        time.sleep(1)
        return await post(url, *args, **kwargs)
