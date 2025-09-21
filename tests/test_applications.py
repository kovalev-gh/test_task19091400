import pytest

BASE = "/api/v1/applications"


@pytest.mark.asyncio
async def test_create_application(client):
    resp = await client.post(f"{BASE}", json={"amount_original": 100, "currency": "USD"})
    print("CREATE RESPONSE:", resp.text)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert float(data["amount_original"]) == 100
    assert data["currency"] == "USD"
    assert "id" in data
    assert "user_id" in data


@pytest.mark.asyncio
async def test_confirm_application(client):
    resp = await client.post(f"{BASE}", json={"amount_original": 100, "currency": "USD"})
    assert resp.status_code == 200, resp.text
    app_id = resp.json()["id"]

    resp2 = await client.post(f"{BASE}/{app_id}/confirm")
    print("CONFIRM RESPONSE:", resp2.text)
    assert resp2.status_code == 200, resp2.text
    data = resp2.json()
    assert data["status"] == "approved"
    assert data["commission_usdt"] is not None
    assert float(data["amount_usdt"]) > 0
    assert "user_id" in data


@pytest.mark.asyncio
async def test_cancel_application(client):
    resp = await client.post(f"{BASE}", json={"amount_original": 50, "currency": "USD"})
    assert resp.status_code == 200, resp.text
    app_id = resp.json()["id"]

    resp2 = await client.post(f"{BASE}/{app_id}/cancel")
    print("CANCEL RESPONSE:", resp2.text)
    assert resp2.status_code == 200, resp2.text
    data = resp2.json()
    assert data["status"] == "cancelled"
    assert "user_id" in data
