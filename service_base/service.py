from __future__ import print_function

import asyncio
import logging
import signal
import threading
from abc import abstractmethod, ABCMeta
from typing import Optional

from service_base.cancellation_token import CancellationToken

TERMINATE_SIGNALS = (signal.SIGINT, signal.SIGTERM)


class Service(metaclass=ABCMeta):
    _cancellation_token: CancellationToken
    _logger: logging.Logger

    def __init__(self, should_stop_on_signal: bool = True):
        self._should_stop_on_signal = should_stop_on_signal

        self._cancellation_token = CancellationToken(canceled=True)
        self._logger = logging.getLogger(type(self).__name__)

    @property
    def is_alive(self) -> bool:
        """
        this property is True, if the service is running.
        """
        return self._is_alive()

    def _is_alive(self) -> bool:
        """
        this may be overridden by child classes to change the 'is_alive' behaviour
        """
        return not self._cancellation_token.is_canceled

    @property
    def name(self) -> str:
        return type(self).__name__

    @property
    def type(self) -> str:
        return "default"

    async def start(self):
        """
        starts the service, and blocks until 'stop' is called
        """
        self._cancellation_token = CancellationToken()  # Create new unset token
        if self._should_stop_on_signal:
            self._register_signals()
        server_exception = None
        try:
            self._logger.info(f"Starting {self.name}...")
            await self._inner_start()
            await self._run_service(cancellation_token=self._cancellation_token)
        except Exception as ex:
            server_exception = ex
            self._logger.debug(f"Exception was thrown", exc_info=ex)
            self._cancellation_token.cancel()
        finally:
            await self._cancellation_token.wait()
            await self._inner_stop(exception=server_exception)
            logging.shutdown()

    def _register_signals(self):
        self._logger.info("Registering Terminate Signals...")
        try:
            loop = asyncio.get_event_loop()
            for sig in TERMINATE_SIGNALS:
                loop.add_signal_handler(sig, lambda: self.stop())
        except NotImplementedError:
            if threading.current_thread() is threading.main_thread():
                for sig in TERMINATE_SIGNALS:
                    signal.signal(sig, lambda s, f: self.stop())
            else:
                self._logger.warning("Can't register signals")

    async def _inner_start(self):
        """
        this method may be implemented by child classes, to perform some initialization logic
        before actually starting the service
        """
        pass

    @abstractmethod
    async def _run_service(self, cancellation_token: CancellationToken):
        """
        this method should be implemented by child classes, and actually run the service
        :param cancellation_token: the cancellation token that will be set when 'stop' is called
        """
        raise NotImplementedError()

    async def _inner_stop(self, exception: Optional[Exception] = None):
        """
        this method may be implemented by child classes, to perform some cleanup logic
        after the service has finished running.
        :param exception: the exception (if any) that _run_service raised
        """
        pass

    def stop(self):
        """
        stops the service (sets the cancellation token, so the service will stop gracefully)
        """
        self._cancellation_token.cancel()
