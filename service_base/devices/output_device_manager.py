from abc import ABCMeta, abstractmethod

from service_base.devices import OutputDevice, EventOutputDevice
from service_base.devices.device_manager import DeviceManager
from service_base.serializers import EventSerializer


class OutputDeviceManager(DeviceManager, metaclass=ABCMeta):
    @abstractmethod
    def get_output_device(self, device_name: str) -> OutputDevice:
        raise NotImplementedError()


class EventOutputDeviceManager(DeviceManager):
    def __init__(self, inner_device_manager: OutputDeviceManager, serializer: EventSerializer):
        super().__init__()

        self._inner_device_manager = inner_device_manager
        self._serializer = serializer

    def get_event_output_device(self, device_name: str) -> EventOutputDevice:
        output_device = self._inner_device_manager.get_output_device(device_name)
        return EventOutputDevice(output_device, self._serializer)
