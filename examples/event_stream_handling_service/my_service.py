import asyncio
import logging

from service_base.event_handling_service import EventHandlingService
from service_base.devices import EventInputDeviceManager

from service_base_events.event import Event


class MyService(EventHandlingService[Event]):
    def __init__(self,
                 input_device_manager: EventInputDeviceManager,
                 **kwargs):
        super().__init__(input_device_manager=input_device_manager, **kwargs)

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
