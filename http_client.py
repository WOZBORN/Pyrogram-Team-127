import aiohttp

from models import User, Rating


class HttpClient:
    def __init__(self):
        self.session = None
        self.host = "https://f18e4325-89f0-4357-b6a4-2221454d52fb-00-24sehfqtbpqxn.janeway.replit.dev"
        self.cache = {}

    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def get_user(self, tg_id: int):
        session = await self._get_session()
        if tg_id in self.cache:
            return self.cache[tg_id]
        async with session.get(f"{self.host}/get_user?tg_id={tg_id}") as response:
            if response.status == 200:
                data = await response.json(content_type=None)
                if data["status"] == 200:
                    user = User(**data["body"]["user"])
                    self.cache[tg_id] = user
                    return user
            return None

    async def create_user(self, tg_id: int, username: str):
        session = await self._get_session()
        url = f"{self.host}/create_user?tg_id={tg_id}&username={username}"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json(content_type=None)
                if data["status"] == 200:
                    user = User(**data["body"]["user"])
                    self.cache[tg_id] = user
                    return user
            return None

    async def get_rating(self):
        session = await self._get_session()
        async with session.get(f"{self.host}/get_rating") as response:
            if response.status == 200:
                data = await response.json(content_type=None)
                if data["status"] == 200:
                    return [Rating(**rating) for rating in data["body"]["rating"]]
            return None

    async def close_session(self):
        if self.session is not None:
            await self.session.close()
