import asyncio
import logging
import operator
from typing import AsyncIterable, Tuple

from service_base.devices import BufferInputDeviceManager
from service_base.messages import InputMessage
from service_base.buffer_stream_handling_service_base import BuffferStreamHandlingServiceBase


class BufferStreamHandlingService(BuffferStreamHandlingServiceBase):
    def __init__(self,
                 input_device_manager: BufferInputDeviceManager,
                 chunk_size: int,
                 **kwargs):
        super().__init__(input_device_manager=input_device_manager, **kwargs)

        self._chunk_size = chunk_size
        self._logger = logging.getLogger("my_service")

    @property
    def name(self) -> str:
        return f"{type(self).__name__}(my_service)"

    def _get_input_name(self) -> str:
        return f"BufferStreamHandlingService"

    async def _handle_stream(self, stream: AsyncIterable[Tuple[bytes, InputMessage]]):
        chunks_gen = chunks(stream, self._chunk_size)
        async for chunk in chunks_gen:
            buffers_getter = operator.itemgetter(0)
            messages_getter = operator.itemgetter(1)
            messages = [messages_getter(chunk_tuple).commit() for chunk_tuple in chunk]
            buffers = [buffers_getter(chunk_tuple) for chunk_tuple in chunk]
            self._logger.info(f"Aggregated {self._chunk_size} test buffers: {buffers}")
            await asyncio.gather(*messages, return_exceptions=True)


async def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    curr = []
    async for x in lst:
        curr.append(x)
        if len(curr) >= n:
            yield curr
            curr = []
    yield curr
