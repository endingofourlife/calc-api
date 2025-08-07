from environs import Env
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

env = Env()
env.read_env('.env')

# DATABASE_URL = URL.create( # for production
#     drivername='postgresql+asyncpg',
#     username=env.str('POSTGRES_USER'),
#     password=env.str('POSTGRES_PASSWORD'),
#     host=env.str('POSTGRES_HOST'),
#     database=env.str('POSTGRES_DB'),
#     port=5432
# ).render_as_string(hide_password=False)
DATABASE_URL = "sqlite+aiosqlite:///database.db" # for testing purposes  TODO: REMOVE AIOSQLITE!!!!

if "sqlite" in DATABASE_URL:
    engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
else:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True
    )

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session