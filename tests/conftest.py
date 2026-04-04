import pytest
import respx

from babybuddy_mcp import client as client_module
from babybuddy_mcp.config import settings


@pytest.fixture(autouse=True)
def mock_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "babybuddy_url", "http://test-babybuddy")
    monkeypatch.setattr(settings, "babybuddy_token", "test-token")


@pytest.fixture(autouse=True)
def reset_client() -> None:
    """Reset the shared httpx client between tests."""
    client_module._client = None


@pytest.fixture
def mock_api() -> respx.MockRouter:
    """Provide a respx router pre-configured for the test babybuddy instance."""
    with respx.mock(base_url="http://test-babybuddy", assert_all_called=False) as router:
        yield router


def paginated(results: list[object]) -> dict[str, object]:
    """Wrap results in DRF pagination envelope."""
    return {"count": len(results), "next": None, "previous": None, "results": results}
