from httpx import AsyncClient


async def test_post_category(ac: AsyncClient):
    response = await ac.post("/category/add", json={
        "id": 2,
        "title": "category2"
    })

    assert response.json()["status"] == "success"


async def test_get_all_category(ac: AsyncClient):
    response = await ac.get("/category/all_category", params={
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 2


async def test_update_category(ac: AsyncClient):
    response = await ac.put("/category/edit?id_category=2", json={
        "title": "new_title_category"
    })

    response_check_new_title = await ac.get("/category/", params={
        "id": 2
    })
    title = response_check_new_title.json()["data"]["title"]

    assert response.status_code == 200
    assert response.json()["status"] == "success"

    assert title == "new_title_category"


async def test_delete_category(prepare_database, ac: AsyncClient):
    response = await ac.delete("/category/delete", params={
        "id_category": "2"
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"

