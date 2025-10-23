import random
import time
import logging
from collections.abc import Generator
from typing import Optional, Union, List

from dify_plugin import LargeLanguageModel
from dify_plugin.entities import I18nObject
from dify_plugin.errors.model import CredentialsValidateFailedError, InvokeError
from dify_plugin.entities.model import AIModelEntity, FetchFrom, ModelType
from dify_plugin.entities.model.llm import LLMResult, LLMResultChunk, LLMResultChunkDelta, LLMUsage
from dify_plugin.entities.model.message import PromptMessage, PromptMessageTool, AssistantPromptMessage

logger = logging.getLogger(__name__)

class MockGptLargeLanguageModel(LargeLanguageModel):
    """
    MockGPT 实现
    """

    def _invoke(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        model_parameters: dict,
        tools: Optional[list[PromptMessageTool]] = None,
        stop: Optional[list[str]] = None,
        stream: bool = True,
        user: Optional[str] = None,
    ) -> Union[LLMResult, Generator]:
        """
        调用大语言模型
        """

        # 模拟响应内容
        demo_responses = [
            "这是一个演示模型的回复。我可以帮助您了解 Dify 插件的工作原理。",
            "作为演示模型，我会生成模拟的响应内容来展示插件功能。",
            "您好！这是 Demo AI 模型的模拟输出，用于演示插件开发流程。"
        ]

        response_text = random.choice(demo_responses)

        if stream:
            return self._handle_stream_response(model, prompt_messages, response_text)
        else:
            return self._handle_sync_response(model, prompt_messages, response_text)
   
    def _handle_stream_response(self, model: str, prompt_messages: List[PromptMessage],
                               response_text: str) -> Generator:
        """
        处理流式响应
        """
        # 模拟流式输出
        words = response_text.split()
        for i, word in enumerate(words):
            chunk_text = word + (" " if i < len(words) - 1 else "")

            delta = LLMResultChunkDelta(
                index=0,
                message=AssistantPromptMessage(content=chunk_text),
                finish_reason=None if i < len(words) - 1 else "stop",
                usage=self._calc_usage(response_text) if i == len(words) - 1 else None
            )

            yield LLMResultChunk(
                model=model,
                prompt_messages=prompt_messages,
                system_fingerprint=None,
                delta=delta
            )

            # 模拟网络延迟
            time.sleep(0.1)

    def _handle_sync_response(self, model: str, prompt_messages: List[PromptMessage],
                             response_text: str) -> LLMResult:
        """
        处理同步响应
        """
        return LLMResult(
            model=model,
            prompt_messages=prompt_messages,
            message=AssistantPromptMessage(content=response_text),
            usage=self._calc_usage(response_text),
            system_fingerprint=None
        )

    def _calc_usage(self, text: str) -> LLMUsage:
        """
        计算使用量（模拟）
        """
        prompt_tokens = 50  # 模拟
        completion_tokens = len(text.split())

        return LLMUsage(
            prompt_tokens=prompt_tokens,
            prompt_unit_price=0.001,
            prompt_price_unit=1000,
            prompt_price=0.00005,
            completion_tokens=completion_tokens,
            completion_unit_price=0.002,
            completion_price_unit=1000,
            completion_price=completion_tokens * 0.000002,
            total_tokens=prompt_tokens + completion_tokens,
            total_price=0.00005 + completion_tokens * 0.000002,
            currency="USD",
            latency=1.5
        )
   
    def get_num_tokens(
        self,
        model: str,
        credentials: dict,
        prompt_messages: list[PromptMessage],
        tools: Optional[list[PromptMessageTool]] = None,
    ) -> int:
        """
        计算 token 数量（模拟）
        """
        total_text = ""
        for message in prompt_messages:
            if isinstance(message.content, str):
                total_text += message.content

        # 简单估算：中文字符算1个token，英文单词算1个token
        return len(total_text.split()) + len([c for c in total_text if '\u4e00' <= c <= '\u9fff'])

    def validate_credentials(self, model: str, credentials: dict) -> None:
        """
        验证模型凭据
        """
        try:
            pass
        except Exception as ex:
            raise CredentialsValidateFailedError(str(ex))

    def get_customizable_model_schema(
        self, model: str, credentials: dict
    ) -> AIModelEntity:
        """
        返回模型 Schema
        """
        entity = AIModelEntity(
            model=model,
            label=I18nObject(zh_Hans=model, en_US=model),
            model_type=ModelType.LLM,
            features=[],
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={},
            parameter_rules=[],
        )

        return entity

    @property
    def _invoke_error_mapping(self) -> dict:
        """
        错误映射
        """
        return {
            InvokeError: [Exception]
        }