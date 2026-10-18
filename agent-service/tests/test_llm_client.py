from unittest.mock import MagicMock

import pytest
from openai import APITimeoutError
from openai.types.chat import ChatCompletion

from app.config import Settings
from app.llm.client import ChatResult, DeepSeekClient, InvalidChatResponseError


@pytest.fixture
def client_and_sdk(monkeypatch):
    sdk = MagicMock()
    constructor = MagicMock(return_value=sdk)
    monkeypatch.setattr("app.llm.client.OpenAI", constructor)
    settings = Settings(
        _env_file=None,
        deepseek_api_key="test-api-key",
        deepseek_model="requested-model",
        deepseek_base_url="https://example.com/v1",
    )
    client = DeepSeekClient(settings)
    constructor.assert_called_once_with(
        api_key="test-api-key",
        base_url="https://example.com/v1",
        timeout=30.0,
        max_retries=0,
    )
    return client, sdk


def completion(content="Hello", usage=True, choices=True):
    return ChatCompletion(
        id="test-completion",
        created=0,
        object="chat.completion",
        model="actual-model",
        choices=[{
            "index": 0,
            "finish_reason": "stop",
            "message": {"role": "assistant", "content": content},
        }] if choices else [],
        usage={"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12}
        if usage else None,
    )


def test_chat_returns_result_and_sends_user_message(client_and_sdk):
    client, sdk = client_and_sdk
    sdk.chat.completions.create.return_value = completion()

    result = client.chat("Hi")

    assert result == ChatResult(
        text="Hello", model="actual-model", input_tokens=10, output_tokens=2
    )
    sdk.chat.completions.create.assert_called_once_with(
        model="requested-model", messages=[{"role": "user", "content": "Hi"}]
    )


@pytest.mark.parametrize("content", [None, "", " \n\t"])
def test_chat_rejects_empty_text(client_and_sdk, content):
    client, sdk = client_and_sdk
    sdk.chat.completions.create.return_value = completion(content=content)

    with pytest.raises(InvalidChatResponseError, match="no text"):
        client.chat("Hi")


def test_chat_rejects_missing_choices(client_and_sdk):
    client, sdk = client_and_sdk
    sdk.chat.completions.create.return_value = completion(choices=False)

    with pytest.raises(InvalidChatResponseError, match="no choices"):
        client.chat("Hi")


def test_chat_rejects_missing_usage(client_and_sdk):
    client, sdk = client_and_sdk
    sdk.chat.completions.create.return_value = completion(usage=False)

    with pytest.raises(InvalidChatResponseError, match="missing token usage"):
        client.chat("Hi")


def test_chat_preserves_zero_token_counts(client_and_sdk):
    client, sdk = client_and_sdk
    response = completion()
    response.usage.prompt_tokens = 0
    response.usage.completion_tokens = 0
    sdk.chat.completions.create.return_value = response

    result = client.chat("Hi")

    assert result.input_tokens == 0
    assert result.output_tokens == 0


def test_chat_propagates_sdk_errors_without_retry(client_and_sdk):
    client, sdk = client_and_sdk
    error = APITimeoutError(request=MagicMock())
    sdk.chat.completions.create.side_effect = error

    with pytest.raises(APITimeoutError) as exc_info:
        client.chat("Hi")

    assert exc_info.value is error
    assert sdk.chat.completions.create.call_count == 1


def test_close_releases_sdk_client(client_and_sdk):
    client, sdk = client_and_sdk

    client.close()

    sdk.close.assert_called_once_with()
