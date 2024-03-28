import asyncpg


class Session:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.pool = None

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(dsn=self.dsn)

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
