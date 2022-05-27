from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic, AsyncIterable, Tuple

from service_base.messages import InputMessage
from service_base.stream_handling_service_base import StreamHandlingServiceBase

from service_base_events.event import Event

TEvent = TypeVar("TEvent", bound=Event)


class EventHandlingService(StreamHandlingServiceBase[TEvent], Generic[TEvent], metaclass=ABCMeta):
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