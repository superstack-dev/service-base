import asyncio
import logging

from service_base.devices.input_device_manager import BufferInputDeviceManager
from service_base.devices.rabbitmq.rabbit_mq_input_device_manager import RabbitMQInputDeviceManager

from single_buffer_handling_service import SingleBufferHandlingService

logging.basicConfig(level="DEBUG")

rabbit_connection_parameters = dict(
    port=5672,
    timeout=10,
    ssl=False,
    host="localhost"
)

input_device_manager = BufferInputDeviceManager(
    RabbitMQInputDeviceManager(max_prefetch_size=1, **rabbit_connection_parameters))


my_service = SingleBufferHandlingService(input_device_manager=input_device_manager)


def main():
    asyncio.run(my_service.start())


if __name__ == "__main__":
    main()
