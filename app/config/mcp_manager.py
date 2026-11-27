import sys
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPManager:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.session: ClientSession | None = None
        self.mcp_tools: list[dict] = []       # Schema đã chuyển sang chuẩn Gemini
        self.tool_names: set[str] = set()     # Lưu tên để phân luồng nhanh

    async def connect(self):
        server_params = StdioServerParameters(
            command=sys.executable,  # Trỏ đúng python.exe của venv hiện tại
            args=["-m", "app.MCPServer.calendar_mcp_server"],
        )

        # Mở và giữ sống kết nối stdio + session qua AsyncExitStack
        read, write = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        await self.session.initialize()

        # Hỏi server danh sách tool và chuyển sang format của Gemini Interactions API
        response = await self.session.list_tools()
        self.mcp_tools = []
        self.tool_names = set()

        for tool in response.tools:
            self.tool_names.add(tool.name)
            self.mcp_tools.append({
                "type": "function",
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.input_schema,
            })

    async def execute_tool(self, name: str, arguments: dict) -> str:
        if not self.session:
            return '{"success": false, "error": "MCP session is not connected"}'

        result = await self.session.call_tool(name, arguments=arguments)
        # Gom nội dung text trả về từ MCP Server
        texts = [
            block.text for block in result.content
            if getattr(block, "type", None) == "text"
        ]
        return "\n".join(texts)

    async def disconnect(self):
        await self.exit_stack.aclose()


# Tạo 1 instance dùng chung trong toàn bộ ứng dụng FastAPI
mcp_manager = MCPManager()