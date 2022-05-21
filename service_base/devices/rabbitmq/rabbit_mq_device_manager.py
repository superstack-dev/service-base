import socket
from typing import Optional, Dict

import aio_pika

from service_base.devices.device_manager import DeviceManager


class RabbitMQDeviceManager(DeviceManager):
    _connection: Optional[aio_pika.Connection]

    def __init__(self, client_properties: Dict[str, str] = None, **connection_parameters):
        super().__init__()

        self._connection_parameters = connection_parameters
        self._client_properties = client_properties

        self._connection = None

    def get_client_properties(self):
        client_properties = self._client_properties or dict()
        client_properties.update({
            "hostname": socket.gethostname()
        })
        return client_properties

    async def get_connection(self) -> aio_pika.Connection:
        if self._connection is None:
            client_properties = self.get_client_properties()
            self._connection = await aio_pika.connect_robust(client_properties=client_properties,
                                                             **self._connection_parameters)

        if self._connection.is_closed:
            await self._connection.connect()

        return self._connection

    async def _inner_connect(self):
        await self.get_connection()

    async def _inner_disconnect(self):
        if self._connection is not None:
            await self._connection.close()
            self._connection = None
