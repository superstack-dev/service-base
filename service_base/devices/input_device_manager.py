from abc import ABCMeta, abstractmethod
from typing import TypeVar, Type

from service_base.devices import InputDevice, EventInputDevice, BufferInputDevice
from service_base.devices.device_manager import DeviceManager
from service_base.serializers import EventSerializer


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


class BufferInputDeviceManager(DeviceManager):
    def __init__(self, inner_device_manager: InputDeviceManager):
        super().__init__()

        self._inner_device_manager = inner_device_manager

    def get_buffer_input_device(self, device_name: str):
        input_device = self._inner_device_manager.get_input_device(device_name)
        return BufferInputDevice(input_device)
