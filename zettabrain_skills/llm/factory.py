"""
LLM Provider Factory - Create providers based on configuration
"""

import os
from typing import Optional
from zettabrain_skills.llm.base import LLMProvider
from zettabrain_skills.llm.providers.ollama import OllamaProvider


def create_llm_provider(
    provider_name: Optional[str] = None,
    **kwargs
) -> LLMProvider:
    """
    Create LLM provider based on configuration

    Args:
        provider_name: Provider to use (ollama, groq, together, bedrock, claude, openai)
                      If None, reads from LLM_PROVIDER env var, defaults to ollama
        **kwargs: Provider-specific configuration

    Returns:
        LLM provider instance

    Environment Variables:
        LLM_PROVIDER: Provider name (default: ollama)
        GROQ_API_KEY: Groq API key
        TOGETHER_API_KEY: Together AI API key
        AWS_ACCESS_KEY_ID: AWS credentials for Bedrock
        ANTHROPIC_API_KEY: Claude API key
        OPENAI_API_KEY: OpenAI API key

    Examples:
        # Use Ollama (default, local)
        provider = create_llm_provider()

        # Use Groq (ultra fast, cheap)
        provider = create_llm_provider("groq")

        # Use Together AI
        provider = create_llm_provider("together")

        # Use AWS Bedrock
        provider = create_llm_provider("bedrock", model_id="meta.llama3-1-8b-instruct-v1:0")
    """

    provider_name = provider_name or os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider_name == "ollama":
        return OllamaProvider(**kwargs)

    elif provider_name == "groq":
        from zettabrain_skills.llm.providers.groq_provider import GroqProvider
        if "model" not in kwargs:
            groq_model = os.getenv("GROQ_MODEL")
            if groq_model:
                kwargs["model"] = groq_model
        return GroqProvider(**kwargs)

    elif provider_name == "together":
        from zettabrain_skills.llm.providers.together_provider import TogetherProvider
        if "model" not in kwargs:
            together_model = os.getenv("TOGETHER_MODEL")
            if together_model:
                kwargs["model"] = together_model
        return TogetherProvider(**kwargs)

    elif provider_name == "bedrock":
        from zettabrain_skills.llm.providers.bedrock_provider import BedrockProvider
        if "model_id" not in kwargs:
            bedrock_model = os.getenv("BEDROCK_MODEL")
            if bedrock_model:
                kwargs["model_id"] = bedrock_model
        if "region" not in kwargs:
            aws_region = os.getenv("AWS_REGION")
            if aws_region:
                kwargs["region"] = aws_region
        return BedrockProvider(**kwargs)

    elif provider_name in ["claude", "anthropic"]:
        try:
            from zettabrain_skills.llm.providers.claude_provider import ClaudeProvider
            return ClaudeProvider(**kwargs)
        except ImportError:
            raise ValueError(
                "Claude provider requires anthropic package: pip install anthropic"
            )

    elif provider_name == "openai":
        try:
            from zettabrain_skills.llm.providers.openai_provider import OpenAIProvider
            return OpenAIProvider(**kwargs)
        except ImportError:
            raise ValueError(
                "OpenAI provider requires openai package: pip install openai"
            )

    else:
        raise ValueError(
            f"Unknown provider: {provider_name}. "
            f"Supported: ollama, groq, together, bedrock, claude, openai"
        )


def get_provider_info() -> dict:
    """Get information about configured provider"""
    provider_name = os.getenv("LLM_PROVIDER", "ollama")

    info = {
        "provider": provider_name,
        "available_providers": ["ollama", "groq", "together", "bedrock", "claude", "openai"],
    }

    # Check which API keys are configured
    if os.getenv("GROQ_API_KEY"):
        info["groq_configured"] = True
    if os.getenv("TOGETHER_API_KEY"):
        info["together_configured"] = True
    if os.getenv("AWS_ACCESS_KEY_ID"):
        info["bedrock_configured"] = True
    if os.getenv("ANTHROPIC_API_KEY"):
        info["claude_configured"] = True
    if os.getenv("OPENAI_API_KEY"):
        info["openai_configured"] = True

    return info
