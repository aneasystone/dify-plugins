from collections.abc import Generator
from typing import Any, Optional

from core.helper.code_executor.code_executor import CodeExecutor, CodeLanguage
from core.tools.builtin_tool.tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.errors import ToolInvokeError


class Add(BuiltinTool):
    def _invoke(
        self,
        user_id: str,
        tool_parameters: dict[str, Any],
        conversation_id: Optional[str] = None,
        app_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        加法运算
        """

        x = tool_parameters.get("x", 0)
        y = tool_parameters.get("y", 0)

        result = str(x + y)
        yield self.create_text_message(result)
