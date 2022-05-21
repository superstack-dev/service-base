from typing import Optional, Dict

import aio_pika
from aio_pika import Message
from pamqp.encode import encode_table_value

from service_base.devices.output_device import OutputDevice
from service_base.devices.rabbitmq.rabbit_mq_device import RabbitMQDevice
from service_base.messages import OutputMessage


def _encode_header_value(value):
    try:
        encode_table_value(value)
        return value
    except TypeError:
        return str(value)


def _flatten_headers_dict(headers: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    items = []
    for key, value in headers.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            items.extend(_flatten_headers_dict(value, new_key, sep=sep).items())
        else:
            if isinstance(value, list):
                items.extend([(new_key + sep + v, True) for v in value if isinstance(v, str)])
            items.append((new_key, _encode_header_value(value)))
    return dict(items)


class RabbitMQOutputDevice(RabbitMQDevice, OutputDevice):
    _exchange: Optional[aio_pika.Exchange]

    def __init__(self,
                 device_manager: "RabbitMQOutputDeviceManager",
                 exchange_name: str):
        super().__init__(device_manager, exchange_name)

        self._device_manager = device_manager
        self._exchange_name = exchange_name

        self._exchange = None

    async def get_exchange(self) -> aio_pika.Exchange:
        if self._exchange is None or self._channel.is_closed:
            channel = await self.get_channel()
            self._exchange = await channel.get_exchange(self._exchange_name, ensure=False)

        return self._exchange

    async def _inner_write(self, message: OutputMessage):
        exchange = await self.get_exchange()
        await exchange.publish(Message(message.getvalue(),
                                       headers=_flatten_headers_dict(message.metadata)),
                               "OUTPUT", mandatory=True)
