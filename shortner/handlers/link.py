from typing import AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from shortner.service import link as link_service
from shortner.schemas.link import CreateLinkRequest, LinkResponse

router = APIRouter(prefix="/links", tags=["links"])
redirect_router = APIRouter(tags=["redirect"])

get_db_dependency = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Wrapper to call the actual get_db_dependency"""
    async for session in get_db_dependency():
        yield session


@router.post("/", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
async def create_link(
    request: CreateLinkRequest,
    session: AsyncSession = Depends(get_session),
) -> LinkResponse:
    """Create a new shortened link"""
    url_entry = await link_service.create_short_link(
        session=session,
        original_url=str(request.original_url),
        ttl_seconds=request.ttl_seconds,
    )
    return LinkResponse.from_orm(url_entry)


@router.get("/{short_code}", response_model=LinkResponse)
async def get_link(
    short_code: str,
    session: AsyncSession = Depends(get_session),
) -> LinkResponse:
    url_entry = await link_service.get_link(session=session, short_code=short_code)
    
    if not url_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link with code '{short_code}' not found",
        )
    
    return LinkResponse.from_orm(url_entry)


@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(
    short_code: str,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a link by short code"""
    deleted = await link_service.delete_link(session=session, short_code=short_code)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link with code '{short_code}' not found",
        )


@redirect_router.get("/{short_code}")
async def redirect_to_url(
    short_code: str,
    session: AsyncSession = Depends(get_session),
):
    url_entry = await link_service.get_link(session=session, short_code=short_code)
    
    if not url_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Short link '{short_code}' not found or has expired",
        )
    
    return RedirectResponse(
        url=url_entry.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
