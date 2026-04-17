import asyncio
from core.database import SessionLocal
from sqlalchemy import text

async def clear():
    async with SessionLocal() as session:
        await session.execute(text('TRUNCATE TABLE interactions'))
        await session.commit()
        print('✅ Database cleared for video!')

if __name__ == "__main__":
    asyncio.run(clear())
