import httpx
import pytest
import respx

from babybuddy_mcp.tools.notes import (
    create_note,
    create_tag,
    delete_note,
    delete_tag,
    list_notes,
    list_tags,
    update_note,
    update_tag,
)

BASE = "http://test-babybuddy"

NOTE = {"id": 1, "child": 1, "note": "First smile!", "time": "2024-01-15T10:00:00Z"}
TAG = {"id": 1, "name": "milestone", "color": "#ff5733"}


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=BASE, assert_all_called=False) as router:
        yield router


async def test_list_notes(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/notes/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [NOTE]}
        )
    )
    result = await list_notes()
    assert result[0]["note"] == "First smile!"


async def test_create_note(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/notes/").mock(return_value=httpx.Response(201, json=NOTE))
    result = await create_note(child_id=1, note="First smile!", time="2024-01-15T10:00:00")
    assert result["id"] == 1


async def test_create_note_with_tags(mock_api: respx.MockRouter) -> None:
    route = mock_api.post("/api/notes/").mock(return_value=httpx.Response(201, json=NOTE))
    await create_note(
        child_id=1, note="First smile!", time="2024-01-15T10:00:00", tags=["milestone"]
    )
    assert b"tags" in route.calls[0].request.content


async def test_update_note(mock_api: respx.MockRouter) -> None:
    mock_api.patch("/api/notes/1/").mock(
        return_value=httpx.Response(200, json={**NOTE, "note": "Updated!"})
    )
    result = await update_note(1, note="Updated!")
    assert result["note"] == "Updated!"


async def test_delete_note(mock_api: respx.MockRouter) -> None:
    mock_api.delete("/api/notes/1/").mock(return_value=httpx.Response(204))
    result = await delete_note(1)
    assert "1" in result


async def test_list_tags(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/tags/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [TAG]}
        )
    )
    result = await list_tags()
    assert result[0]["name"] == "milestone"


async def test_create_tag(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/tags/").mock(return_value=httpx.Response(201, json=TAG))
    result = await create_tag(name="milestone", color="#ff5733")
    assert result["color"] == "#ff5733"


async def test_update_tag(mock_api: respx.MockRouter) -> None:
    mock_api.patch("/api/tags/1/").mock(
        return_value=httpx.Response(200, json={**TAG, "color": "#00ff00"})
    )
    result = await update_tag(1, color="#00ff00")
    assert result["color"] == "#00ff00"


async def test_delete_tag(mock_api: respx.MockRouter) -> None:
    mock_api.delete("/api/tags/1/").mock(return_value=httpx.Response(204))
    result = await delete_tag(1)
    assert "1" in result
