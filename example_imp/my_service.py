

import asyncio
import logging
from dataclasses import dataclass

from pyservice.event import Event
from pyservice.event_handling_service import EventHandlingService
from pyservice.devices import EventInputDeviceManager, EventOutputDeviceManager


@dataclass
class ServiceConfig:
    input_device_manager: EventInputDeviceManager
    output_device_manager: EventOutputDeviceManager


class MyService(EventHandlingService[Event]):
    def __init__(self,
                 config: ServiceConfig,
                 **kwargs):
        super().__init__(input_device_manager=config.input_device_manager, **kwargs)

        self._output_device_manager = config.output_device_manager
        self._output_device_name = config.output_device_name

        self._logger = logging.getLogger("my_service")

    @property
    def name(self) -> str:
        return f"{type(self).__name__}(my_service)"

    @property
    def type(self) -> str:
        return "my_service"

    def _get_input_name(self) -> str:
        return f"MyService"

    async def _handle_event(self, event: Event):

        try:
            self._logger.info(f"Test event: {event}")
            await asyncio.sleep(2)
        except:
            raise
