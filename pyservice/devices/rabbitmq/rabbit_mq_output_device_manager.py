from typing import Optional

from pyservice.devices.output_device_manager import OutputDeviceManager
from pyservice.devices.rabbitmq.rabbit_mq_device_manager import RabbitMQDeviceManager
from pyservice.devices.rabbitmq.rabbit_mq_output_device import RabbitMQOutputDevice


class RabbitMQOutputDeviceManager(RabbitMQDeviceManager, OutputDeviceManager):
    def __init__(self, **connection_parameters):
        super().__init__(**connection_parameters)

    def get_output_device(self, device_name: str) -> RabbitMQOutputDevice:
        return RabbitMQOutputDevice(self, device_name)
