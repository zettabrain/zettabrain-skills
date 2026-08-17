"""
Base LLM provider interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Iterator


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @abstractmethod
    def generate(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000, **kwargs
    ) -> str:
        """
        Generate text using the LLM

        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific parameters

        Returns:
            Generated text
        """
        pass

    @abstractmethod
    def stream(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000, **kwargs
    ) -> Iterator[str]:
        """
        Stream generated text token by token

        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific parameters

        Yields:
            Text chunks as they are generated
        """
        pass

    @abstractmethod
    def check_health(self) -> bool:
        """
        Check if the LLM provider is available and healthy

        Returns:
            True if healthy, False otherwise
        """
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model

        Returns:
            Dictionary with model information (name, size, context_length, etc.)
        """
        pass
