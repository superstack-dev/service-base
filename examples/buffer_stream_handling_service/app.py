import asyncio
import logging

from service_base.devices import BufferInputDeviceManager
from service_base.devices.rabbitmq import RabbitMQInputDeviceManager

from buffer_stream_handling_service import BufferStreamHandlingService


logging.basicConfig(level="DEBUG")

rabbit_connection_parameters = dict(
    port=5672,
    timeout=10,
    ssl=False,
    host="localhost"
)

input_device_manager = BufferInputDeviceManager(
    RabbitMQInputDeviceManager(max_prefetch_size=5, **rabbit_connection_parameters))


my_service = BufferStreamHandlingService(input_device_manager=input_device_manager, chunk_size=5)


def main():
    asyncio.run(my_service.start())


if __name__ == "__main__":
    main()
