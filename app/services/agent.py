import json
from app.config.settings import settings
from app.config.llm import client
from app.schemas.tools import tools
from app.tool.tool_map import TOOL_MAPS
from app.prompts.system import system_instruction


model_name = settings.MODEL_NAME

def invoke_AI(content: str, max_call: int = 5):
    response = client.interactions.create(
                model=model_name,
                input=content,
                tools=tools,
                system_instruction=system_instruction
            )
    for i in range(max_call):  
        function_call = [
            step for step in response.steps if step.type == "function_call"
        ]
        if(not function_call):
            break
        tool_response = []
        for call in function_call:
            print("function_call")
            if(call.type == "function_call"):
                args = call.arguments
                function = TOOL_MAPS.get(f'{call.name}') 
                try:
                    result = function(**args)
                except Exception as e:
                    result = {"success": False, "error": str(e)}
            tool_response.append(
                {
                    "type": "function_result",
                    "name": call.name,
                    "call_id": call.id,
                    "result": [
                        {
                            "type": "text", 
                            "text": json.dumps(result)
                        }
                    ],
                }
            )
            print(tool_response)
            response = client.interactions.create(
                model=model_name,
                previous_interaction_id=response.id,
                input=tool_response,
                tools=tools,
                system_instruction=system_instruction
            )    
    return response.output_text
    
print(invoke_AI("remind me on 25/11/2026 at 2pm that i will have a meeting"))