import asyncpg


class Session:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.pool = None

    async def connect(self) -> None:
        try:
            self.pool = await asyncpg.create_pool(dsn=self.dsn)
        except Exception as e:
            print(f"Error creating connection pool: {e}")
            return

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
