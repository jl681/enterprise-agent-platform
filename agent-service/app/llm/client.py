from openai import OpenAI
from pydantic import BaseModel, Field

from app.config import Settings


class ChatResult(BaseModel):
    text: str = Field(min_length=1)
    model: str = Field(min_length=1)
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)


class InvalidChatResponseError(ValueError):
    """The provider returned an incomplete or unusable chat response."""


class DeepSeekClient:
    def __init__(self, settings: Settings):
        self._model = settings.deepseek_model
        self._client = OpenAI(
            api_key=settings.deepseek_api_key.get_secret_value(),
            base_url=settings.deepseek_base_url,
            timeout=30.0,
            max_retries=0,
        )

    def chat(self, message: str) -> ChatResult:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": message}],
        )
        if not response.choices:
            raise InvalidChatResponseError("Model response contains no choices")

        text = response.choices[0].message.content
        if text is None or not text.strip():
            raise InvalidChatResponseError("Model response contains no text")

        usage = response.usage
        if (
            usage is None
            or usage.prompt_tokens is None
            or usage.completion_tokens is None
        ):
            raise InvalidChatResponseError("Model response is missing token usage")

        return ChatResult(
            text=text,
            model=response.model,
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
        )

    def close(self) -> None:
        self._client.close()
