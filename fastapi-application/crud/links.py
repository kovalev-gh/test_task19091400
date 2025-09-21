from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from core.models import MerchantTraderLink, Application, User
from core.schemas.links import LinkCreate, LinkUpdate
from typing import List


async def create_link(db: AsyncSession, data: LinkCreate) -> MerchantTraderLink:
    # проверяем, что merchant существует
    res = await db.execute(select(User).where(User.id == data.merchant_id))
    merchant = res.scalar_one_or_none()
    if not merchant:
        raise HTTPException(400, f"Merchant {data.merchant_id} not found")

    # проверяем, что trader существует
    res = await db.execute(select(User).where(User.id == data.trader_id))
    trader = res.scalar_one_or_none()
    if not trader:
        raise HTTPException(400, f"Trader {data.trader_id} not found")

    link = MerchantTraderLink(**data.model_dump())
    db.add(link)
    await db.commit()
    await db.refresh(link)
    return link


async def list_links(
    db: AsyncSession,
    merchant_id: int | None = None,
    trader_id: int | None = None,
) -> List[MerchantTraderLink]:
    stmt = select(MerchantTraderLink)
    if merchant_id:
        stmt = stmt.where(MerchantTraderLink.merchant_id == merchant_id)
    if trader_id:
        stmt = stmt.where(MerchantTraderLink.trader_id == trader_id)
    res = await db.execute(stmt)
    return res.scalars().all()


async def update_link(
    db: AsyncSession,
    link_id: int,
    data: LinkUpdate,
) -> MerchantTraderLink:
    res = await db.execute(
        select(MerchantTraderLink).where(MerchantTraderLink.id == link_id)
    )
    link = res.scalar_one_or_none()
    if not link:
        raise HTTPException(404, "link not found")

    # если обновляем merchant_id — проверим
    if data.merchant_id is not None:
        res = await db.execute(select(User).where(User.id == data.merchant_id))
        if not res.scalar_one_or_none():
            raise HTTPException(400, f"Merchant {data.merchant_id} not found")

    # если обновляем trader_id — проверим
    if data.trader_id is not None:
        res = await db.execute(select(User).where(User.id == data.trader_id))
        if not res.scalar_one_or_none():
            raise HTTPException(400, f"Trader {data.trader_id} not found")

    for k, v in data.model_dump(exclude_none=True).items():
        setattr(link, k, v)

    await db.commit()
    await db.refresh(link)
    return link


async def assign_trader(
    db: AsyncSession,
    merchant_id: int,
    application: Application,
) -> int | None:
    """Назначить трейдера для заявки с учётом приоритета и веса (берём максимальный вес)"""
    res = await db.execute(
        select(MerchantTraderLink).where(
            MerchantTraderLink.merchant_id == merchant_id,
            MerchantTraderLink.status == "active",
        )
    )
    links = res.scalars().all()

    # фильтруем по валюте
    links = [
        link
        for link in links
        if application.currency.upper() in (link.currencies or "").split(",")
    ]
    if not links:
        return None

    # сортировка по приоритету
    links.sort(key=lambda l: l.priority)

    # берём минимальный приоритет
    min_priority = links[0].priority
    candidates = [l for l in links if l.priority == min_priority]

    # выбираем трейдера с максимальным весом
    chosen = max(candidates, key=lambda l: l.weight)

    return chosen.trader_id
