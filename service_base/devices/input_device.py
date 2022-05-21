from abc import ABCMeta, abstractmethod
from typing import AsyncIterable, Tuple, TypeVar, Type, Generic, Optional

from aiostream import operator, streamcontext

from service_base.utils import cancellable_aiter
from service_base.cancellation_token import CancellationToken
from service_base.devices.device import Device
from service_base.messages import InputMessage
from service_base.serializers import EventSerializer


class InputDevice(Device, metaclass=ABCMeta):
    async def read(self, cancellation_token: CancellationToken, timeout: Optional[int] = None) -> \
            AsyncIterable[InputMessage]:
        if not self._started:
            raise Exception("Can not consume from input device that has not been started yet.")

        async for message in cancellable_aiter(self._inner_read(cancellation_token, timeout), cancellation_token):
            yield message

    @abstractmethod
    async def _inner_read(self, cancellation_token: CancellationToken, timeout: Optional[int] = None) -> \
            AsyncIterable[InputMessage]:
        raise NotImplementedError()


TEvent = TypeVar("TEvent")


@operator
async def _deserialize_stream(source, serializer: EventSerializer, event_type: Type[TEvent]):
    async with streamcontext(source) as streamer:
        async for message in streamer:  # type: InputMessage
            try:
                yield serializer.deserialize(message, event_type), message
            except:
                await message.rollback()
                raise


class EventInputDevice(Generic[TEvent], Device):
    def __init__(self, inner_device: InputDevice, serializer: EventSerializer, event_type: Type[TEvent]):
        super().__init__(inner_device.name)

        self._inner_device = inner_device
        self._serializer = serializer
        self._event_type = event_type

    async def _inner_connect(self):
        await self._inner_device.connect()

    async def read_event(self, cancellation_token: CancellationToken, timeout: Optional[int] = None) -> \
            AsyncIterable[Tuple[TEvent, InputMessage]]:
        if not self._started:
            raise Exception("Can not read from device that has not been started yet.")

        deserialized_stream = _deserialize_stream(self._inner_device.read(cancellation_token, timeout), self._serializer,
                                                  self._event_type)
        async with deserialized_stream.stream() as iterator:
            async for event, message in iterator:
                yield event, message

    async def _inner_disconnect(self) -> None:
        await self._inner_device.disconnect()
