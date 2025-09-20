from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from core.models import MerchantTraderLink
from core.schemas.links import LinkCreate, LinkUpdate
from typing import List


async def create_link(db: AsyncSession, data: LinkCreate) -> MerchantTraderLink:
    link = MerchantTraderLink(**data.model_dump())
    db.add(link)
    await db.commit()
    await db.refresh(link)
    return link


async def list_links(db: AsyncSession, merchant_id: int | None = None, trader_id: int | None = None) -> List[MerchantTraderLink]:
    stmt = select(MerchantTraderLink)
    if merchant_id:
        stmt = stmt.where(MerchantTraderLink.merchant_id == merchant_id)
    if trader_id:
        stmt = stmt.where(MerchantTraderLink.trader_id == trader_id)
    res = await db.execute(stmt)
    return res.scalars().all()


async def update_link(db: AsyncSession, link_id: int, data: LinkUpdate) -> MerchantTraderLink:
    res = await db.execute(select(MerchantTraderLink).where(MerchantTraderLink.id == link_id))
    link = res.scalar_one_or_none()
    if not link:
        raise HTTPException(404, "link not found")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(link, k, v)
    await db.commit()
    await db.refresh(link)
    return link
