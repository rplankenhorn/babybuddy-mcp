from typing import Annotated

from fastmcp import FastMCP

from ..client import api_get, api_list, api_patch, api_post

mcp = FastMCP("children")


@mcp.tool
async def list_children() -> list[dict[str, object]]:
    """List all child profiles. Always call this first to get child IDs needed by other tools."""
    return await api_list("children")


@mcp.tool
async def get_child(
    child_id: Annotated[int, "ID of the child to retrieve"],
) -> dict[str, object]:
    """Get a single child profile by ID."""
    return await api_get(f"children/{child_id}")


@mcp.tool
async def create_child(
    first_name: Annotated[str, "Child's first name"],
    last_name: Annotated[str, "Child's last name"],
    birth_date: Annotated[str, "Date of birth in YYYY-MM-DD format (e.g. 2024-01-15)"],
    birth_time: Annotated[str | None, "Time of birth in HH:MM:SS format (optional)"] = None,
) -> dict[str, object]:
    """Add a new child profile."""
    data: dict[str, object] = {
        "first_name": first_name,
        "last_name": last_name,
        "birth_date": birth_date,
    }
    if birth_time is not None:
        data["birth_time"] = birth_time
    return await api_post("children", data)


@mcp.tool
async def update_child(
    child_id: Annotated[int, "ID of the child to update"],
    first_name: Annotated[str | None, "New first name"] = None,
    last_name: Annotated[str | None, "New last name"] = None,
    birth_date: Annotated[str | None, "New birth date in YYYY-MM-DD format"] = None,
    birth_time: Annotated[str | None, "New birth time in HH:MM:SS format"] = None,
) -> dict[str, object]:
    """Update a child's profile. Only provided fields are changed."""
    data: dict[str, object] = {}
    if first_name is not None:
        data["first_name"] = first_name
    if last_name is not None:
        data["last_name"] = last_name
    if birth_date is not None:
        data["birth_date"] = birth_date
    if birth_time is not None:
        data["birth_time"] = birth_time
    return await api_patch("children", child_id, data)
