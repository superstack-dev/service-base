import asyncio
from typing import Optional


class CancellationToken:
    _event: asyncio.Event

    def __init__(self, canceled: Optional[bool] = False):
        self._event = asyncio.Event()

        if canceled:
            self._event.set()

    def cancel(self):
        self._event.set()

    async def wait(self):
        return await self._event.wait()

    @property
    def is_canceled(self):
        return self._event.is_set()
