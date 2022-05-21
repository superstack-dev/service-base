from service_base.devices.input_device_manager import InputDeviceManager
from service_base.devices.rabbitmq.rabbit_mq_device_manager import RabbitMQDeviceManager
from service_base.devices.rabbitmq.rabbit_mq_input_device import RabbitMQInputDevice


class RabbitMQInputDeviceManager(RabbitMQDeviceManager, InputDeviceManager):
    def __init__(self,
                 max_prefetch_size: int = 1,
                 **connection_parameters):
        super().__init__(**connection_parameters)

        self._max_prefetch_size = max_prefetch_size

    def get_input_device(self, device_name: str) -> RabbitMQInputDevice:
        return RabbitMQInputDevice(self, device_name, self._max_prefetch_size)
