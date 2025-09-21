import pytest

BASE_LINKS = "/api/v1/links"
BASE_APPS = "/api/v1/applications"


@pytest.mark.asyncio
async def test_assign_trader_link_creation(client):
    """Создаём линк merchant↔trader"""
    resp = await client.post(
        BASE_LINKS,
        json={
            "merchant_id": 1,
            "trader_id": 1,
            "status": "active",
            "priority": 1,
            "weight": 10,
            "currencies": "USD,USDT",
        },
    )
    print("LINK CREATE RESPONSE:", resp.text)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert int(data["merchant_id"]) == 1
    assert int(data["trader_id"]) == 1
    assert int(data["priority"]) == 1
    assert int(data["weight"]) == 10
    assert "USD" in data["currencies"]


@pytest.mark.asyncio
async def test_assign_trader_to_application(client):
    """Создаём заявку и назначаем трейдера"""
    resp = await client.post(
        BASE_APPS,
        json={"amount_original": 100, "currency": "USD"},
    )
    assert resp.status_code == 200, resp.text
    app_id = resp.json()["id"]

    resp2 = await client.post(f"{BASE_APPS}/{app_id}/assign-trader")
    print("ASSIGN TRADER RESPONSE:", resp2.text)
    assert resp2.status_code == 200, resp2.text
    data = resp2.json()
    assert int(data["id"]) == app_id
    assert data["trader_id"] is not None
    assert "email" in data or data["trader_id"] == 1
