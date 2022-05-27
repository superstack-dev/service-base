import asyncio
import logging

from service_base.single_buffer_handling_service_base import SingleBufferHandlingServiceBase
from service_base.devices import BufferInputDeviceManager


class SingleBufferHandlingService(SingleBufferHandlingServiceBase):
    def __init__(self,
                 input_device_manager: BufferInputDeviceManager,
                 **kwargs):
        super().__init__(input_device_manager=input_device_manager, **kwargs)

        self._logger = logging.getLogger("single_buffer_handling_service")

    @property
    def name(self) -> str:
        return f"{type(self).__name__}(single_buffer_handling_service)"

    def _get_input_name(self) -> str:
        return f"SingleBufferHandlingService"

    async def _handle_buffer(self, buffer: bytes):

        try:
            self._logger.info(f"Test buffer: {buffer}")
            await asyncio.sleep(2)
        except:
            raise
