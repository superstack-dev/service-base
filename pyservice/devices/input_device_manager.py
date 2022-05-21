from abc import ABCMeta, abstractmethod
from typing import TypeVar, Type

from pyservice.devices import InputDevice, EventInputDevice
from pyservice.devices.device_manager import DeviceManager
from pyservice.serializers import EventSerializer


class InputDeviceManager(DeviceManager, metaclass=ABCMeta):
    @abstractmethod
    def get_input_device(self, device_name: str) -> InputDevice:
        raise NotImplementedError()


TResult = TypeVar("TResult")


class EventInputDeviceManager(DeviceManager):
    def __init__(self, inner_device_manager: InputDeviceManager, serializer: EventSerializer):
        super().__init__()

        self._inner_device_manager = inner_device_manager
        self._serializer = serializer

    def get_event_input_device(self, device_name: str, event_type: Type[TResult]):
        input_device = self._inner_device_manager.get_input_device(device_name)
        return EventInputDevice(input_device, self._serializer, event_type)
