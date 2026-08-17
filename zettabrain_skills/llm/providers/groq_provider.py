"""
Groq API Provider - Ultra-fast inference with open source models
https://groq.com/
"""

import os
from typing import Dict, Any, Optional
import httpx
from rich.console import Console

console = Console()


class GroqProvider:
    """Groq API provider for ultra-fast LLM inference"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "llama-3.1-8b-instant",
        base_url: str = "https://api.groq.com/openai/v1",
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Get one at https://console.groq.com"
            )

        self.model = model
        self.base_url = base_url
        self.timeout = timeout

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate text using Groq API"""

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        **kwargs,
                    },
                )
                response.raise_for_status()
                result = response.json()

                return {
                    "content": result["choices"][0]["message"]["content"],
                    "model": result["model"],
                    "tokens_used": result["usage"]["total_tokens"],
                    "provider": "groq",
                }

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise Exception(
                    "Invalid Groq API key. Get one at https://console.groq.com"
                )
            elif e.response.status_code == 429:
                raise Exception(
                    "Groq rate limit exceeded. Upgrade your plan or wait."
                )
            else:
                raise Exception(f"Groq API error: {e.response.text}")

        except httpx.TimeoutException:
            raise Exception(f"Groq request timed out after {self.timeout}s")

        except Exception as e:
            raise Exception(f"Groq generation failed: {e}")

    def check_health(self) -> bool:
        """Check if Groq API is accessible"""
        try:
            with httpx.Client(timeout=10) as client:
                response = client.get(
                    f"{self.base_url}/models",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                    },
                )
                return response.status_code == 200
        except Exception:
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about current model configuration"""
        return {
            "provider": "Groq",
            "model": self.model,
            "base_url": self.base_url,
            "api_key_set": bool(self.api_key),
        }


# Available Groq models
GROQ_MODELS = {
    "llama-3.1-8b-instant": "Llama 3.1 8B - Fast and efficient",
    "llama-3.1-70b-versatile": "Llama 3.1 70B - More capable, slower",
    "mixtral-8x7b-32768": "Mixtral 8x7B - Great for long context",
    "gemma2-9b-it": "Gemma 2 9B - Google's model",
}
