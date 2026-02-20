from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# رابط قاعدة البيانات (تأكدي من مطابقة البيانات لجهازك)
DATABASE_URL = "postgresql+asyncpg://postgres:132003@localhost/hospital_monitoring"

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# وظيفة لجلب جلسة قاعدة البيانات
async def get_db():
    async with SessionLocal() as session:
        yield session