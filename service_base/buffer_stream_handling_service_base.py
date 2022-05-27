from abc import abstractmethod, ABCMeta
from typing import Optional, Type, get_args,  AsyncIterable,  Tuple

from service_base import Service
from service_base.cancellation_token import CancellationToken
from service_base.devices import BufferInputDeviceManager
from service_base.messages import InputMessage


class BuffferStreamHandlingServiceBase(Service, metaclass=ABCMeta):
    """
    An abstract class that can be used to create subclasses which are services that continuously read buffers from an input device. Subclasses must implement the _handle_stream method which provides the stream of buffers. This can, for example, be used to aggregate and then handle raw input data in any desired way.
    """

    def __init__(self, input_device_manager: BufferInputDeviceManager, read_timeout: Optional[int] = None, **kwargs):
        super().__init__(**kwargs)

        self._input_device_manager = input_device_manager
        self._read_timeout = read_timeout

    async def _inner_start(self):
        await self._input_device_manager.connect()

    @abstractmethod
    def _get_input_name(self) -> str:
        raise NotImplementedError()

    def _get_input_type(self) -> Type[bytes]:
        return get_args(type(self).__orig_bases__[0])[0]

    @abstractmethod
    async def _handle_stream(self, stream: AsyncIterable[Tuple[bytes, InputMessage]]):
        raise NotImplementedError()

    async def _run_service(self, cancellation_token: CancellationToken):
        input_device_name = self._get_input_name()
        async with self._input_device_manager.get_buffer_input_device(input_device_name,
                                                                      ) as input_device:
            self._logger.info(f"Starting to listen on '{input_device_name}'")
            while not self._cancellation_token.is_canceled:
                input_stream = input_device.yield_buffer_and_message(cancellation_token, self._read_timeout)
                try:
                    await self._handle_stream(input_stream)
                except Exception as exc:
                    self._logger.error(f"Error has occurred while handling stream", exc_info=exc)

    async def _inner_stop(self, exception: Optional[Exception] = None):
        await self._input_device_manager.disconnect()
