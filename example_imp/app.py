import asyncio
import logging
import time
from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse

from my_service import MyService, ServiceConfig
from pyservice.cancellation_token import CancellationToken

from pyservice.devices.input_device_manager import EventInputDeviceManager
from pyservice.devices.output_device_manager import EventOutputDeviceManager
from pyservice.devices.rabbitmq.rabbit_mq_input_device_manager import RabbitMQInputDeviceManager
from pyservice.devices.rabbitmq.rabbit_mq_output_device_manager import RabbitMQOutputDeviceManager
from pyservice.event import Event
from pyservice.serializers.json_serializer import JsonSerializer


def _get_rabbitmq_connection_parameters():

    params = dict(
        port=5672,
        timeout=10,
        ssl=False,
        host="my-rabbit"
    )
    return params


logging.basicConfig(level="DEBUG")

app = FastAPI()

rabbit_connection_parameters = _get_rabbitmq_connection_parameters()

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


@app.get("/event")
async def root(req: Request, res: Response):
    logging.info("Test Message Production")

    output_device = my_service._output_device_manager.get_event_output_device(my_service._output_device_name)

    await output_device.connect()
    await output_device.write_event(Event())

    return {"test": "finished"}


@app.get("/run")
async def root(req: Request, res: Response):

    if my_service.is_alive:
        return {"start-run": "not started because service is alive"}

    await my_service.start()

    background_tasks = BackgroundTasks()
    background_tasks.add_task(my_service._run_service, my_service._cancellation_token)

    return JSONResponse("start-run finished", background=background_tasks)


@app.get("/stop")
async def root(req: Request, res: Response):
    if not my_service.is_alive:
        return {"stop-run": "not needed because service is not alive"}

    my_service.stop()

    return {"stop-run": "successful"}
