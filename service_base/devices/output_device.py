from abc import ABCMeta, abstractmethod

from service_base.devices import Device
from service_base.messages import OutputMessage
from service_base.serializers import EventSerializer

from service_base_events.event import Event


class OutputDevice(Device, metaclass=ABCMeta):
    async def write(self, message: OutputMessage) -> None:
        if not self._started:
            raise Exception("Can not publish to output device that has not been started yet.")

        await self._inner_write(message)

    @abstractmethod
    async def _inner_write(self, event: OutputMessage):
        raise NotImplementedError()


class EventOutputDevice(Device):
    def __init__(self, inner_device: OutputDevice, serializer: EventSerializer):
        super().__init__(inner_device.name)

        self._inner_device = inner_device
        self._serializer = serializer

    async def _inner_connect(self):
        await self._inner_device.connect()

    async def write_event(self, event: Event) -> None:
        if not self._started:
            raise Exception("Can not publish to output device that has not been started yet.")

        message = self._serializer.serialize(event)
        await self._inner_device.write(message)

    async def _inner_disconnect(self) -> None:
        await self._inner_device.disconnect()
