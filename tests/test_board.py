from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import AsyncClient

async def test_post_category_for_board_test(ac: AsyncClient):
    response = await ac.post("/category/add", json={
        "id": 1,
        "title": "category",
    })

    assert response.status_code == 200, "Ошибка, категория для поста не добавилась"


async def test_post_board(ac: AsyncClient):
    """инициализируем в т.ч. кэширование"""
    FastAPICache.init(RedisBackend("redis://localhost:6379"))

    response = await ac.post("/board/add", json={
        "id": 6,
        "title": "post1",
        "text": "post1",
        "price": 123,
        "photo": "str",
        "date": "2024-01-22T10:40:19.401",
        "category_id": 1,
    })

    assert response.status_code == 200, "Ошибка, пост не создался"


async def test_get_board_on_id(ac: AsyncClient):
    response = await ac.get("/board/", params={
        "id": 6
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["id"] == 6


async def test_get_board_on_category(ac: AsyncClient):
    response = await ac.get("/board/board_in_category", params={
        "board_category": 1
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 1


async def test_edit_board(ac: AsyncClient):
    response = await ac.put("/board/edit?id_card=6", json={
        "title": "new_title"
    })

    response_check_new_title = await ac.get("/board/", params={
        "id": 6
    })
    title = response_check_new_title.json()["data"]["title"]

    assert response.status_code == 200
    assert response.json()["status"] == "success"
  #  assert title == "new_title"
