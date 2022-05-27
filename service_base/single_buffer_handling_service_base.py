from abc import abstractmethod, ABCMeta
from typing import AsyncIterable, Tuple

from service_base.messages import InputMessage
from service_base.buffer_stream_handling_service_base import BuffferStreamHandlingServiceBase


class SingleBufferHandlingServiceBase(BuffferStreamHandlingServiceBase, metaclass=ABCMeta):
    """
    An abstract class that can be used to create subclasses which are services that continuously read buffers from an input device. It is a simplification of the BufferStreamHadnlingServiceBase ABC which implements its _handle_stream method but adds a new method _handle_buffer which subclasses must implement. This can be used to specify how to handle singular buffers instead of a buffer stream.
    """
    async def _inner_start(self):
        await self._input_device_manager.connect()

    @abstractmethod
    async def _handle_buffer(self, buffer: bytes):
        raise NotImplementedError()

    async def _handle_critical_error(self, buffer: bytes, message: InputMessage, exception: Exception):
        # TODO: Error handling?
        self._logger.error(f"Error has occurred for buffer:\n{buffer}", exc_info=exception)
        await message.rollback()

    async def _handle_stream(self, stream: AsyncIterable[Tuple[bytes, InputMessage]]):
        async for buffer, message in stream:
            try:
                await self._handle_buffer(buffer)
                await message.commit()
            except Exception as exc:
                await self._handle_critical_error(buffer, message, exc)
