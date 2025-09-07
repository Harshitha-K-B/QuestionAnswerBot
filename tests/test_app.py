import pytest
from unittest.mock import MagicMock
import streamlit as st
from openai import OpenAI

# Import your app's code if needed
# from app import some_function   # if you extract functions from app.py

# Mock OpenAI client
@pytest.fixture
def mock_openai(monkeypatch):
    client = OpenAI(api_key="fake-key")
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked response"

    def fake_chat_completion(*args, **kwargs):
        return mock_response

    monkeypatch.setattr(client.chat.completions, "create", fake_chat_completion)
    return client


def test_add_user_message():
    # Simulate session state
    messages = [{"role": "system", "content": "You are a helper."}]
    user_input = "Hello bot!"

    messages.append({"role": "user", "content": user_input})

    assert messages[-1]["role"] == "user"
    assert messages[-1]["content"] == "Hello bot!"


def test_openai_response(mock_openai):
    response = mock_openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )

    assert response.choices[0].message.content == "Mocked response"
