"""Service layer for URL operations"""

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from shortner.repo import url as url_repo
from shortner.utils.base62 import generate_short_code
from shortner.models.url import URL


async def create_short_link(
    session: AsyncSession,
    original_url: str,
    ttl_seconds: int | None = None,
) -> URL:
    """Create a new shortened link with optional TTL"""
    short_code = generate_short_code(length=6)
    
    expires_at = None
    if ttl_seconds:
        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
    
    url_entry = await url_repo.create_url(
        session=session,
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at,
    )
    
    await session.commit()
    await session.refresh(url_entry)
    return url_entry


async def get_link(session: AsyncSession, short_code: str) -> URL | None:
    """Get a link by short code"""
    url_entry = await url_repo.get_url_by_short_code(session, short_code)
    
    if not url_entry:
        return None
    
    # Check if link has expired
    if url_entry.expires_at and datetime.utcnow() > url_entry.expires_at:
        await url_repo.delete_url(session, short_code)
        await session.commit()
        return None
    
    # Increment clicks
    await url_repo.increment_clicks(session, short_code)
    await session.commit()
    
    return url_entry


async def delete_link(session: AsyncSession, short_code: str) -> bool:
    """Delete a link by short code"""
    deleted = await url_repo.delete_url(session, short_code)
    await session.commit()
    return deleted
