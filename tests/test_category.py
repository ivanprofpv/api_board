from httpx import AsyncClient


async def test_post_category(ac: AsyncClient):
    response = await ac.post("/category/add", json={
        "id": 2,
        "title": "category2"
    })

    assert response.json()["status"] == "success"


async def test_get_category(ac: AsyncClient):
    response = await ac.get("/category/", params={
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 2