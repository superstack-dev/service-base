import asyncio
import logging

from service_base.single_event_handling_service_base import SingleEventHandlingServiceBase
from service_base.devices import EventInputDeviceManager

from service_base_events.event import Event


class SingleEventHandlingService(SingleEventHandlingServiceBase[Event]):
    def __init__(self,
                 input_device_manager: EventInputDeviceManager,
                 **kwargs):
        super().__init__(input_device_manager=input_device_manager, **kwargs)

        self._logger = logging.getLogger("single_event_handling_service")

    @property
    def name(self) -> str:
        return f"{type(self).__name__}(single_event_handling_service)"

    def _get_input_name(self) -> str:
        return f"SingleEventHandlingService"

    async def _handle_event(self, event: Event):

        try:
            self._logger.info(f"Test event: {event}")
            await asyncio.sleep(2)
        except:
            raise
