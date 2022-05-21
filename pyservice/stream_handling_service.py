from abc import abstractmethod, ABCMeta
from typing import Optional, Type, TypeVar, Generic, get_args, Callable, AsyncIterable, Awaitable, Tuple

from aiostream import operator, streamcontext

from pyservice.event import Event
from pyservice import Service
from pyservice.cancellation_token import CancellationToken
from pyservice.devices import EventInputDeviceManager
from pyservice.messages import InputMessage

TEvent = TypeVar("TEvent", bound=Event)


class StreamHandlingService(Service, Generic[TEvent], metaclass=ABCMeta):
    def __init__(self, input_device_manager: EventInputDeviceManager, read_timeout: Optional[int] = None, **kwargs):
        super().__init__(**kwargs)

        self._input_device_manager = input_device_manager
        self._read_timeout = read_timeout

    async def _inner_start(self):
        await self._input_device_manager.connect()

    @abstractmethod
    def _get_input_name(self) -> str:
        raise NotImplementedError()

    def _get_input_type(self) -> Type[TEvent]:
        return get_args(type(self).__orig_bases__[0])[0]

    @abstractmethod
    async def _handle_stream(self, stream: AsyncIterable[Tuple[TEvent, InputMessage]]):
        raise NotImplementedError()

    async def _run_service(self, cancellation_token: CancellationToken):
        input_device_name = self._get_input_name()
        input_event_type = self._get_input_type()
        async with self._input_device_manager.get_event_input_device(input_device_name,
                                                                     input_event_type) as input_device:
            self._logger.info(f"Starting to listen on '{input_device_name}'")
            while not self._cancellation_token.is_canceled:
                input_stream = input_device.read_event(cancellation_token, self._read_timeout)
                try:
                    await self._handle_stream(input_stream)
                except Exception as exc:
                    self._logger.error(f"Error has occurred while handling stream", exc_info=exc)

    async def _inner_stop(self, exception: Optional[Exception] = None):
        await self._input_device_manager.disconnect()
