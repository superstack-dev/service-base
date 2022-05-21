import asyncio
from typing import Optional

import aio_pika

from pyservice.devices.device import Device
from pyservice.devices.rabbitmq.rabbit_mq_device_manager import RabbitMQDeviceManager


class RabbitMQDevice(Device):
    _channel: Optional[aio_pika.Channel]

    def __init__(self, device_manager: RabbitMQDeviceManager, name: str):
        super().__init__(name)

        self._device_manager = device_manager
        self._name = name
        self._channel = None

    @property
    def name(self):
        return self._name

    async def get_channel(self) -> aio_pika.Channel:
        if self._channel is None or self._channel.is_closed:
            connection = await self._device_manager.get_connection()
            self._channel = await connection.channel()

        return self._channel

    async def _inner_connect(self):
        await self.get_channel()

    async def _inner_disconnect(self):
        if self._channel is not None:
            await self._channel.close()
            self._channel = None
