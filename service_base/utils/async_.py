import asyncio
from collections import AsyncIterator

from aiostream.aiter_utils import aiter, anext

from service_base import CancellationToken


async def cancellable_aiter(async_iterator: AsyncIterator, cancellation_token: CancellationToken) -> AsyncIterator:
    cancellation_task = asyncio.create_task(cancellation_token.wait())
    iterator = aiter(async_iterator)
    stop_iteration = False
    while not cancellation_token.is_canceled and not stop_iteration:
        done, pending = await asyncio.wait(
            [cancellation_task, anext(iterator)],
            return_when=asyncio.FIRST_COMPLETED
        )
        for done_task in done:
            if done_task == cancellation_task:
                for pending_task in pending:
                    pending_task.cancel()
                break
            else:
                try:
                    yield done_task.result()
                except StopAsyncIteration:
                    stop_iteration = True
