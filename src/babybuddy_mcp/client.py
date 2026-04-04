from __future__ import annotations

import httpx

from .config import settings

_client: httpx.AsyncClient | None = None

QueryParams = dict[str, str | int | float | bool | None]

__all__ = ["api_delete", "api_get", "api_list", "api_patch", "api_post", "QueryParams"]


def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            base_url=settings.babybuddy_url.rstrip("/"),
            headers={"Authorization": f"Token {settings.babybuddy_token}"},
            timeout=settings.request_timeout,
        )
    return _client


async def api_get(path: str, params: QueryParams | None = None) -> dict[str, object]:
    client = get_client()
    response = await client.get(f"/api/{path}/", params=params)
    response.raise_for_status()
    result = response.json()
    assert isinstance(result, dict)
    return result


async def api_list(
    path: str,
    params: QueryParams | None = None,
) -> list[dict[str, object]]:
    """GET a list endpoint, optionally following DRF pagination.
    
    Only follows pagination if no explicit limit is provided in params.
    This prevents infinite loops when the API ignores the limit parameter.
    """
    client = get_client()
    all_results: list[dict[str, object]] = []
    url = f"/api/{path}/"
    query: QueryParams = dict(params or {})
    
    # Check if user explicitly provided a limit
    has_limit = "limit" in query

    while url:
        response = await client.get(url, params=query)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        all_results.extend(results)
        
        # Stop if user provided a limit - they asked for specific number of results
        if has_limit:
            break
            
        # After the first request params are encoded in the next URL
        query = {}
        url = data.get("next") or ""

    return all_results


async def api_post(path: str, data: dict[str, object]) -> dict[str, object]:
    client = get_client()
    response = await client.post(f"/api/{path}/", json=data)
    response.raise_for_status()
    result = response.json()
    assert isinstance(result, dict)
    return result


async def api_patch(path: str, record_id: int, data: dict[str, object]) -> dict[str, object]:
    client = get_client()
    response = await client.patch(f"/api/{path}/{record_id}/", json=data)
    response.raise_for_status()
    result = response.json()
    assert isinstance(result, dict)
    return result


async def api_delete(path: str, record_id: int) -> None:
    client = get_client()
    response = await client.delete(f"/api/{path}/{record_id}/")
    response.raise_for_status()
