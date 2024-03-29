import asyncio
import time

from config.settings import DSN
from database.session import DataBaseManager


async def main():
    db_manager = DataBaseManager(DSN)
    await db_manager.connect()
    start = time.time()
    await db_manager.extract_dates()
    end = time.time()
    execution_time = end - start
    await db_manager.close()

    print(execution_time)


asyncio.run(main())
