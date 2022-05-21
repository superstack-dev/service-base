import logging
from abc import ABCMeta


class DeviceManager(metaclass=ABCMeta):
    def __init__(self):
        self._started = False
        self._stop_called = False
        self._logger = logging.getLogger(type(self).__name__)

    @property
    def is_started(self) -> bool:
        return self._started

    @property
    def name(self):
        return type(self).__name__

    async def connect(self):
        if self._started:
            raise Exception(f"Device Manager '{self.name}' is already running.")

        self._logger.debug(f"Starting device manager '{self.name}'")
        await self._inner_connect()
        self._started = True

    async def _inner_connect(self):
        pass

    async def __aenter__(self):
        await self.connect()
        return self

    async def disconnect(self) -> None:
        if not self.is_started:
            raise Exception(f"Can not stop device manager '{self.name}' that has not been started yet.")

        if self._stop_called:
            return

        self._stop_called = True
        self._logger.debug(f"Stopping device manager '{self.name}'")
        await self._inner_disconnect()

    async def _inner_disconnect(self) -> None:
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
