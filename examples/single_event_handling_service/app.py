import asyncio
import logging

from service_base.devices.input_device_manager import EventInputDeviceManager
from service_base.devices.rabbitmq.rabbit_mq_input_device_manager import RabbitMQInputDeviceManager
from service_base.serializers.json_serializer import JsonSerializer

from single_event_handling_service import SingleEventHandlingService


logging.basicConfig(level="DEBUG")

rabbit_connection_parameters = dict(
    port=5672,
    timeout=10,
    ssl=False,
    host="localhost"
)

input_device_manager = EventInputDeviceManager(
    RabbitMQInputDeviceManager(max_prefetch_size=1, **rabbit_connection_parameters),
    serializer=JsonSerializer())


my_service = SingleEventHandlingService(input_device_manager=input_device_manager)


def main():
    asyncio.run(my_service.start())


if __name__ == "__main__":
    main()
