from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas.links import LinkCreate, LinkUpdate, LinkRead
from core.auth import get_current_user
from core.models.db_helper import db_helper
from crud import links as crud_links

#router = APIRouter(prefix="/api/v1/links", tags=["Links"])
router = APIRouter()

@router.post("", response_model=LinkRead)
async def create(data: LinkCreate, db: AsyncSession = Depends(db_helper.session_getter), _: dict = Depends(get_current_user)):
    return await crud_links.create_link(db, data)


@router.get("", response_model=list[LinkRead])
async def list_links(merchant_id: int | None = None, trader_id: int | None = None, db: AsyncSession = Depends(db_helper.session_getter), _: dict = Depends(get_current_user)):
    return await crud_links.list_links(db, merchant_id, trader_id)


@router.patch("/{link_id}", response_model=LinkRead)
async def update(link_id: int, data: LinkUpdate, db: AsyncSession = Depends(db_helper.session_getter), _: dict = Depends(get_current_user)):
    return await crud_links.update_link(db, link_id, data)
