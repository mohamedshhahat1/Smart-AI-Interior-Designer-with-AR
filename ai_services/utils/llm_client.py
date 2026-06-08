import os
import json
import asyncio
import logging

logger = logging.getLogger(__name__)

_openai_client = None
_gemini_model = None
_initialized = False


def _init():
    global _openai_client, _gemini_model, _initialized
    if _initialized:
        return
    _initialized = True

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            import openai
            _openai_client = openai.AsyncOpenAI(api_key=api_key)
            logger.info("LLM client: OpenAI initialized")
        except ImportError:
            logger.warning("openai package not installed")

    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key and _openai_client is None:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            _gemini_model = genai.GenerativeModel("gemini-1.5-pro")
            logger.info("LLM client: Gemini initialized")
        except ImportError:
            logger.warning("google-generativeai package not installed")


def is_available() -> bool:
    _init()
    return _openai_client is not None or _gemini_model is not None


async def get_llm_response(messages: list[dict], max_tokens: int = 500) -> str | None:
    _init()

    if _openai_client is not None:
        try:
            response = await _openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.4,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("OpenAI call failed: %s", e)
            return None

    if _gemini_model is not None:
        try:
            combined = "\n".join(
                f"{msg['role']}: {msg['content']}" for msg in messages
            )
            response = _gemini_model.generate_content(combined)
            return response.text
        except Exception as e:
            logger.error("Gemini call failed: %s", e)
            return None

    return None


def get_llm_response_sync(messages: list[dict], max_tokens: int = 500) -> str | None:
    if not is_available():
        return None

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        return None

    try:
        return asyncio.run(get_llm_response(messages, max_tokens))
    except Exception as e:
        logger.error("Sync LLM call failed: %s", e)
        return None


def parse_llm_json(response: str | None) -> dict | None:
    if not response:
        return None
    try:
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
        return json.loads(cleaned)
    except (json.JSONDecodeError, Exception):
        return None
