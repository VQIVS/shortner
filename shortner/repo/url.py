from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from shortner.models.url import URL


async def create_url(
    session: AsyncSession,
    original_url: str,
    short_code: str,
    expires_at: datetime | None = None,
) -> URL:
    url_entry = URL(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at,
    )
    session.add(url_entry)
    await session.flush()
    return url_entry


async def get_url_by_short_code(session: AsyncSession, short_code: str) -> URL | None:
    result = await session.execute(
        select(URL).where(URL.short_code == short_code)
    )
    return result.scalar_one_or_none()


async def get_url_by_id(session: AsyncSession, url_id: int) -> URL | None:
    result = await session.execute(
        select(URL).where(URL.id == url_id)
    )
    return result.scalar_one_or_none()


async def delete_url(session: AsyncSession, short_code: str) -> bool:
    url_entry = await get_url_by_short_code(session, short_code)
    if url_entry:
        await session.delete(url_entry)
        await session.flush()
        return True
    return False


async def increment_clicks(session: AsyncSession, short_code: str) -> None:
    """Increment click count for a short code"""
    url_entry = await get_url_by_short_code(session, short_code)
    if url_entry:
        url_entry.clicks += 1
        await session.flush()
