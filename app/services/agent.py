import json
from app.config.settings import settings
from app.config.llm import client
from app.schemas.tools import tools
from app.tool.tool_map import TOOL_MAPS
from app.config.mcp_manager import mcp_manager
from app.prompts.system import system_instruction


model_name = settings.MODEL_NAME

async def invoke_AI(content: str, max_call: int = 5):
    external_tools = tools + mcp_manager.mcp_tools
    
    response = client.interactions.create(
                model=model_name,
                input=content,
                tools=external_tools,
                system_instruction=system_instruction
            )
    for i in range(max_call):  
        function_call = [
            step for step in response.steps if step.type == "function_call"
        ]
        if(not function_call):
            break
        tool_response = []
        # apply function call to exteranl tool and mcp tool
        for call in function_call:
            args = call.arguments
            if call.name in TOOL_MAPS:
                print(f"funtion tool called: {call.name}")
                function = TOOL_MAPS.get(f'{call.name}') 
                try:
                    result = json.dumps(function(**args), ensure_ascii=False)
                except Exception as e:
                    result = json.dumps({"success": False, "error": str(e)})
            if call.name in mcp_manager.tool_names:
                print(f"mcp tool called: {call.name}")
                try:
                    result = await mcp_manager.execute_tool(call.name, args)
                except Exception as e:
                    result = json.dumps({"success": False, "error": str(e)})
                print(f"mcp args: {args}")
                print(f"mcp response: {result}")
            tool_response.append(
                {
                    "type": "function_result",
                    "name": call.name,
                    "call_id": call.id,
                    "result": [
                        {
                            "type": "text", 
                            "text": result
                        }
                    ],
                }
            )
            response = client.interactions.create(
                model=model_name,
                previous_interaction_id=response.id,
                input=tool_response,
                tools=external_tools,
                system_instruction=system_instruction
            )    
    return response.output_text
    