system_instruction = "you are a personal assistant. Your job is to remember your master's information and do what he want. usually, you should end your response with 'master'."


tools = [
    {
        "type": "google_search",
        "description": "Search any information that is not your master's information."
    },
    {
        "type": "function",
        "name": "save_event",
        "description": "Save an upcoming event with its title, detailed description, and scheduled date/time into memory",
        "defer_loading": True,
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "short and clear about the event. Straight to the main point of the event"
                    },
                "description": {
                    "type": "string",
                    "description": "detailed note about the event." 
                    },
                "date": {
                    "type": "string",
                    "format": "datetime",
                    "description": "Date and time of the event in ISO 8601 format (e.g., '2026-11-25T14:30:00+07:00')"
                    },
            },
            "required": ["title", "description", "date"],
        },
    },
]