import asyncio
import logging

from service_base.devices.input_device_manager import EventInputDeviceManager
from service_base.devices.output_device_manager import EventOutputDeviceManager
from service_base.devices.rabbitmq.rabbit_mq_input_device_manager import RabbitMQInputDeviceManager
from service_base.devices.rabbitmq.rabbit_mq_output_device_manager import RabbitMQOutputDeviceManager
from service_base.serializers.json_serializer import JsonSerializer

from my_service import MyService, ServiceConfig


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

output_device_manager = EventOutputDeviceManager(
    RabbitMQOutputDeviceManager(**rabbit_connection_parameters),
    serializer=JsonSerializer())

service_config = ServiceConfig(input_device_manager, output_device_manager)
# Exchange name
service_config.output_device_name = ""

my_service = MyService(service_config)


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(my_service.start())
    except KeyboardInterrupt as e:
        print("Caught keyboard interrupt. Canceling tasks...")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    main()
