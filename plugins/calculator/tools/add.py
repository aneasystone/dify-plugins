from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class AddTool(Tool):
    
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:    
        """
        加法运算
        """

        x = tool_parameters.get("x", 0)
        y = tool_parameters.get("y", 0)

        result = str(x + y)
        yield self.create_text_message(result)
