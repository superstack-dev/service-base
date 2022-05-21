from typing import TypeVar, Type

from pyservice.messages import InputMessage, OutputMessage
from pyservice.serializers import EventSerializer

from pyservice_events.event import Event

TResult = TypeVar("TResult", bound=Event)


class JsonSerializer(EventSerializer):
    # TODO: Add support for other product types
    def serialize(self, event: Event) -> OutputMessage:
        return OutputMessage(event.serialize().encode(), metadata=event.get_metadata())

    def deserialize(self, message: InputMessage, result_type: Type[TResult]) -> TResult:
        return result_type.deserialize(message.getvalue())
