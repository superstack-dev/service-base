from typing import List, Any, Dict
from uuid import UUID, uuid4

import pydantic
from pydantic import BaseModel, Field


Metadata = Dict[str, Any]


class Event(BaseModel):
    class Config:
        allow_population_by_alias = True
        extra = "allow"

    id: UUID = None
    root_id: UUID = None
    parent_ids: List[UUID] = Field(default_factory=list)

    def attach_child(self, child: 'Event'):
        child.parent_ids.append(self.id)
        child.root_id = self.root_id

    def dict(self, *args, **kwargs):
        dct = super().dict(*args, **kwargs)
        dct["_type"] = self.type
        return dct

    @property
    def type(self):
        if hasattr(self, "_type"):
            return getattr(self, "_type")

        return type(self).__name__

    def get_metadata(self) -> Metadata:
        return dict(type=self.type,
                    id=self.id,
                    parent_ids=[str(parent_id) for parent_id in self.parent_ids],
                    root_id=self.root_id)

    @pydantic.validator('id', pre=True, always=True)
    @classmethod
    def default_ts_id(cls, id_):
        return id_ or uuid4()

    @pydantic.validator('root_id', pre=True, always=True)
    @classmethod
    def default_ts_root_id(cls, root_id, *, values, **kwargs):
        return root_id or values['id']

    def serialize(self):
        return self.json()

    @classmethod
    def deserialize(cls, obj):
        return cls.parse_raw(obj)
