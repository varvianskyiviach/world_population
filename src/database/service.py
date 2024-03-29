from config.settings import TABLE_NAME
from database.session import Session


class Service(Session):
    table_name = TABLE_NAME

    def __init__(self, dsn: str) -> None:
        super().__init__(dsn)

    async def create_table(self) -> None:
        async with self.pool.acquire() as connection:
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id SERIAL PRIMARY KEY,
                    country_name VARCHAR(255) UNIQUE NOT NULL,
                    population INTEGER NOT NULL,
                    region VARCHAR(255) NOT NULL
                );"""
            await connection.execute(create_table_query)
