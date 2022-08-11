import aiohttp
from typing import Optional


class SendCommand:
    def __init__(self, token):
        self.token = token

    def _build_url(self, command: str):
        return f'https://api.telegram.org/bot{self.token}/{command}'

    async def getUpdates(self, timeout: int = 0, offset: Optional[int] = 0) -> dict:
        """
        Receiving updates (messages) of the bot.
        """
        url = self._build_url('getUpdates')
        params = {}
        if offset:
            params['offset'] = offset
        if timeout:
            params['timeout'] = timeout
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as responce:
                return await responce.json()
