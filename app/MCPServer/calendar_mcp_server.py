from mcp.server.mcpserver import MCPServer
import sys
from googleapiclient.errors import HttpError
from typing import Annotated
from pydantic import Field
from app.services.google_auth_service import get_google_service

mcp = MCPServer("calendar MCP server")

def formater(calendar: dict): 
    response = {
        "Success": True,
        "id": calendar.get("id"),
        "description": calendar.get("summary"),
        "startTime": calendar.get("start"), 
        "endTime": calendar.get("end"), 
    }
    return response

@mcp.tool()
async def get_event(
    timeMin: Annotated[str, Field(description="minimum end time to query an event in RFC3339 timestamp format, default value today if user does not request time")], 
    timeMax: Annotated[str, Field(description="Maximum end time to query an event in RFC3339 timestamp format")] = None,  
    maxResults: Annotated[int, Field(description="Maximum end time to query an event in RFC3339 timestamp format")] = 5
): 
    """get upcoming user's event list
        Args:
            time_min: Start of the time range in RFC3339 timestamp format with timezone (e.g., '2011-06-03T10:00:00-07:00').
            time_max: Optional end of the time range in RFC3339 timestamp format with timezone (e.g., '2011-06-03T10:00:00-07:00').
            max_results: Maximum number of events to return (default 10).
    """
    param = {
        "timeMax": timeMax,
        "timeMin": timeMin,
        "calendarId": "primary",
        "maxResults": maxResults,
        "singleEvents": True
    }
    try:
        service = get_google_service("calendar")
        res = service.events().list(**param).execute()
        event = [formater(s) for s in res.get("items")]
        return event
    except HttpError as e:
        print(f"[calendar_mcp] HttpError in list_events: {e}", file=sys.stderr)
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"[calendar_mcp] Error in list_events: {e}", file=sys.stderr)
        return {"success": False, "error": str(e)}
    
    
@mcp.tool()
async def insert_event(
    summary: Annotated[str, Field(description="Short title of the event")],
    description: Annotated[str, Field(description="Optional detailed note for the event.")],
    startTime: Annotated[str, Field(description="Start date/time in RFC3339 timestamp format with timezone (e.g., '2026-11-25T14:00:00+07:00').")],
    endTime: Annotated[str, Field(description="End date/time in RFC3339 timestamp format with timezone (e.g., '2026-11-25T14:00:00+07:00'). Default value should be startTime but an hours later.")],
    location: Annotated[str, Field(description="Place that occured the event")] | None
):
    """Create a new event on the user's primary Google Calendar.

    Args:
        summary: Short title of the event.
        location: Place that occured the event.
        start: Start date/time in ISO 8601 format with timezone (e.g., '2026-11-25T14:00:00+07:00').
        end_iso: End date/time in ISO 8601 format with timezone (e.g., '2026-11-25T15:00:00+07:00').
        description: Optional detailed note for the event.
    """
    param = {
        "calendarId": "primary",
        "body": {
            "summary": summary,
            "description": description,
            "location": location,
            "start": {
                "dateTime": startTime,
                "timeZone": "Asia/Ho_Chi_Minh",
            },
            "end": {
                "dateTime": endTime,
                "timeZone": "Asia/Ho_Chi_Minh",
            }
        }
    }
    try:
        service = get_google_service("calendar")
        res = service.events().insert(**param).execute()
        event = [formater(s) for s in res.get("items")]
        return event
    except HttpError as e:
        print(f"[calendar_mcp] HttpError in create_event: {e}", file=sys.stderr)
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"[calendar_mcp] Error in create_event: {e}", file=sys.stderr)
        return {"success": False, "error": str(e)}
    
    
@mcp.tool()
async def update_event(
    eventId: Annotated[str, Field(description="Target Event Id")],
    summary: Annotated[str, Field(description="Short title of the event")] = None,
    description: Annotated[str, Field(description="Optional detailed note for the event.")] = None,
    location: Annotated[str, Field(description="Place that occured the event")] = None,
    startTime: Annotated[str, Field(description="Start date/time in RFC3339 timestamp format with timezone (e.g., '2026-11-25T14:00:00+07:00').")] = None,
    endTime: Annotated[str, Field(description="End date/time in RFC3339 timestamp format with timezone (e.g., '2026-11-25T14:00:00+07:00').")] = None
):
    """Update an exist event on the user's primary Google Calendar. 

    Args:
        eventId: Target Event Id
        summary: Short title of the event.
        location: Place that occured the event.
        start: Start date/time in ISO 8601 format with timezone (e.g., '2026-11-25T14:00:00+07:00').
        end_iso: End date/time in ISO 8601 format with timezone (e.g., '2026-11-25T15:00:00+07:00').
        description: Optional detailed note for the event.
    """
    param = {
        "calendarId": "primary",
        "eventId": eventId,
        "body": {
            "summary": summary,
            "description": description,
            "location": location,
            "start": {
                "dateTime": startTime,
                "timeZone": "Asia/Ho_Chi_Minh",
            },
            "end": {
                "dateTime": endTime,
                "timeZone": "Asia/Ho_Chi_Minh",
            }
        }
    }
    try:
        service = get_google_service("calendar")
        res = service.events().update(**param).execute()
        return formater(res)
    except HttpError as e:
        print(f"[calendar_mcp] HttpError in update_event: {e}", file=sys.stderr)
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"[calendar_mcp] Error in update_event: {e}", file=sys.stderr)
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")