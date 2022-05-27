from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic, AsyncIterable, Tuple

from service_base.messages import InputMessage
from service_base.stream_handling_service_base import StreamHandlingServiceBase

from service_base_events.event import Event

TEvent = TypeVar("TEvent", bound=Event)


class EventHandlingService(StreamHandlingServiceBase[TEvent], metaclass=ABCMeta):
    """
    An abstract class that can be used to create subclasses which are services that continuously read events from an input device. It is a simplification of the StreamHandlingServiceBase ABC which implements its _handle_stream method but adds a new method _handle_event which subclasses must implement. This can be used to specify how to handle singular events instead of an event stream.
    """
    async def _inner_start(self):
        await self._input_device_manager.connect()

    @abstractmethod
    async def _handle_event(self, event: TEvent):
        raise NotImplementedError()

    async def _handle_critical_error(self, event: TEvent, message: InputMessage, exception: Exception):
        # TODO: Error handling?
        self._logger.error(f"Error has occurred for event:\n{event}", exc_info=exception)
        await message.rollback()

    async def _handle_stream(self, stream: AsyncIterable[Tuple[TEvent, InputMessage]]):
        async for event, message in stream:
            try:
                await self._handle_event(event)
                await message.commit()
            except Exception as exc:
                await self._handle_critical_error(event, message, exc)
