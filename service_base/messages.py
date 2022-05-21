from io import BufferedIOBase, BytesIO
from typing import Dict, Any, Optional

Metadata = Dict[str, Any]


class Message(BufferedIOBase):
    def __init__(self, body: bytes, metadata: Optional[Metadata] = None):
        self._body = BytesIO(body)
        if metadata is None:
            self._metadata = dict()
        else:
            self._metadata = metadata

    @property
    def buffer(self) -> BytesIO:
        return BytesIO(self._body.getvalue())

    def seek(self, offset: int, whence: int = None) -> int:
        return self._body.seek(offset, whence)

    def tell(self) -> int:
        return self._body.tell()

    def read(self, size: int = None):
        return self._body.read(size)

    def getvalue(self) -> bytes:
        return self._body.getvalue()

    @property
    def metadata(self) -> Metadata:
        return self._metadata


class InputMessage(Message):
    async def commit(self):
        pass

    async def rollback(self, exception: Optional[Exception] = None):
        pass


class OutputMessage(Message):
    pass
