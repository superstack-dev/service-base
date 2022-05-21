from abc import ABCMeta, abstractmethod
from typing import TypeVar, Type

from pyservice.messages import OutputMessage, InputMessage

from pyservice_events.event import Event

TResult = TypeVar("TResult")


class EventSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, event: Event) -> OutputMessage:
        raise NotImplementedError()

    @abstractmethod
    def deserialize(self, message: InputMessage, result_type: Type[TResult]) -> TResult:
        raise NotImplementedError()
