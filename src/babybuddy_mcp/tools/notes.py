from typing import Annotated

from fastmcp import FastMCP

from ..client import api_delete, api_list, api_patch, api_post

mcp = FastMCP("notes")


# ── Notes ─────────────────────────────────────────────────────────────────────


@mcp.tool
async def list_notes(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    date_min: Annotated[str | None, "Start of date range, YYYY-MM-DD"] = None,
    date_max: Annotated[str | None, "End of date range, YYYY-MM-DD"] = None,
    limit: Annotated[int, "Maximum number of records to return"] = 50,
) -> list[dict[str, object]]:
    """List notes with optional filters."""
    params: dict[str, object] = {"limit": limit}
    if child_id is not None:
        params["child"] = child_id
    if date_min is not None:
        params["date_min"] = date_min
    if date_max is not None:
        params["date_max"] = date_max
    return await api_list("notes", params)


@mcp.tool
async def create_note(
    child_id: Annotated[int, "ID of the child. Use list_children to get IDs."],
    note: Annotated[str, "The note text content"],
    time: Annotated[str, "Time of the note in ISO 8601 format (e.g. 2024-01-15T14:30:00)"],
    tags: Annotated[list[str] | None, "List of tag names to apply to this note"] = None,
) -> dict[str, object]:
    """Create a new note for a child."""
    data: dict[str, object] = {"child": child_id, "note": note, "time": time}
    if tags is not None:
        data["tags"] = tags
    return await api_post("notes", data)


@mcp.tool
async def update_note(
    note_id: Annotated[int, "ID of the note to update"],
    note: Annotated[str | None, "New note text"] = None,
    time: Annotated[str | None, "New time in ISO 8601 format"] = None,
    tags: Annotated[list[str] | None, "New list of tag names (replaces existing tags)"] = None,
) -> dict[str, object]:
    """Update an existing note. Only provided fields are changed."""
    data: dict[str, object] = {}
    if note is not None:
        data["note"] = note
    if time is not None:
        data["time"] = time
    if tags is not None:
        data["tags"] = tags
    return await api_patch("notes", note_id, data)


@mcp.tool
async def delete_note(
    note_id: Annotated[int, "ID of the note to permanently delete"],
) -> str:
    """Delete a note. This action is permanent."""
    await api_delete("notes", note_id)
    return f"Note {note_id} deleted successfully."


# ── Tags ──────────────────────────────────────────────────────────────────────


@mcp.tool
async def list_tags() -> list[dict[str, object]]:
    """List all available tags that can be applied to notes."""
    return await api_list("tags")


@mcp.tool
async def create_tag(
    name: Annotated[str, "Tag name"],
    color: Annotated[str | None, "Tag color as a hex code (e.g. #ff5733)"] = None,
) -> dict[str, object]:
    """Create a new tag."""
    data: dict[str, object] = {"name": name}
    if color is not None:
        data["color"] = color
    return await api_post("tags", data)


@mcp.tool
async def update_tag(
    tag_id: Annotated[int, "ID of the tag to update"],
    name: Annotated[str | None, "New tag name"] = None,
    color: Annotated[str | None, "New color as a hex code (e.g. #ff5733)"] = None,
) -> dict[str, object]:
    """Update an existing tag. Only provided fields are changed."""
    data: dict[str, object] = {}
    if name is not None:
        data["name"] = name
    if color is not None:
        data["color"] = color
    return await api_patch("tags", tag_id, data)


@mcp.tool
async def delete_tag(
    tag_id: Annotated[int, "ID of the tag to permanently delete"],
) -> str:
    """Delete a tag. This action is permanent and removes the tag from all notes."""
    await api_delete("tags", tag_id)
    return f"Tag {tag_id} deleted successfully."
