import asyncio
from typing import AsyncIterable, Optional

import aio_pika

from service_base.cancellation_token import CancellationToken
from service_base.messages import InputMessage
from service_base.devices.input_device import InputDevice
from service_base.devices.rabbitmq.rabbit_mq_device import RabbitMQDevice


class RabbitMQInputMessage(InputMessage):
    def __init__(self, rabbit_mq_message: aio_pika.IncomingMessage):
        super().__init__(rabbit_mq_message.body, rabbit_mq_message.headers)
        self._rabbit_mq_message = rabbit_mq_message

    async def commit(self):
        self._rabbit_mq_message.ack()

    async def rollback(self, exception: Optional[Exception] = None):
        self._rabbit_mq_message.nack()


class RabbitMQInputDevice(RabbitMQDevice, InputDevice):
    _amqp_queue: Optional[aio_pika.Queue]

    def __init__(self, device_manager: "RabbitMQInputDeviceManager", queue_name: str, max_prefetch_size: int = 1):
        super().__init__(device_manager, queue_name)

        self._device_manager = device_manager
        self._queue_name = queue_name
        self._max_prefetch_size = max_prefetch_size

        self._amqp_queue = None
        self._queue = asyncio.Queue()
        self._consumer_tag = None

    async def on_message(self, message: aio_pika.IncomingMessage):
        await self._queue.put(message)

    async def consume(self):
        queue = await self.get_queue()
        self._consumer_tag = await queue.consume(
            self.on_message,
            arguments=self._device_manager.get_client_properties()
        )

    async def get_channel(self) -> aio_pika.Channel:
        channel = await super(RabbitMQInputDevice, self).get_channel()
        await channel.set_qos(self._max_prefetch_size)
        return channel

    async def get_queue(self) -> aio_pika.Queue:
        if self._amqp_queue is None or self._channel.is_closed:
            channel = await self.get_channel()
            self._amqp_queue = await channel.get_queue(self._queue_name, ensure=True)

        return self._amqp_queue

    async def _inner_connect(self):
        if self._consumer_tag is None:
            await self.consume()

    async def _inner_read(self, cancellation_token: CancellationToken, timeout: Optional[int] = None) -> AsyncIterable[InputMessage]:
        if not self._consumer_tag:
            await self.consume()
        while not cancellation_token.is_canceled:
            try:
                message = await asyncio.wait_for(
                    self._queue.get(),
                    timeout=timeout
                )
                yield RabbitMQInputMessage(message)
            except asyncio.exceptions.TimeoutError:
                break
