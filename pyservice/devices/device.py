import logging
from abc import ABCMeta, abstractmethod


class Device(metaclass=ABCMeta):
    def __init__(self, name: str):
        self._started = False
        self._stop_called = False
        self._logger = logging.getLogger(type(self).__name__)
        self._name = name

    @property
    def is_started(self) -> bool:
        return self._started

    @property
    def name(self):
        return self._name

    async def connect(self):
        if self._started:
            raise Exception(f"Device '{self.name}' is already running.")

        self._logger.debug(f"Starting device '{self.name}'")
        await self._inner_connect()
        self._started = True

    async def _inner_connect(self):
        pass

    async def __aenter__(self):
        await self.connect()
        return self

    async def disconnect(self) -> None:
        if not self.is_started:
            raise Exception(f"Can not stop device '{self.name}' that has not been started yet.")

        if self._stop_called:
            return

        self._stop_called = True
        self._logger.debug(f"Stopping device '{self.name}'")
        await self._inner_disconnect()

    async def _inner_disconnect(self) -> None:
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
