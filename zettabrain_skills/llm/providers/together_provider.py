"""
Together AI Provider - Fast and affordable open source models
https://together.ai/
"""

import os
from typing import Dict, Any, Optional
import httpx
from rich.console import Console

console = Console()


class TogetherProvider:
    """Together AI provider for fast open source LLM inference"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        base_url: str = "https://api.together.xyz/v1",
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "TOGETHER_API_KEY not found. Get one at https://together.ai"
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
        """Generate text using Together AI"""

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
                    "provider": "together",
                }

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise Exception(
                    "Invalid Together API key. Get one at https://together.ai"
                )
            elif e.response.status_code == 429:
                raise Exception(
                    "Together rate limit exceeded. Check your plan."
                )
            else:
                raise Exception(f"Together API error: {e.response.text}")

        except httpx.TimeoutException:
            raise Exception(f"Together request timed out after {self.timeout}s")

        except Exception as e:
            raise Exception(f"Together generation failed: {e}")

    def check_health(self) -> bool:
        """Check if Together API is accessible"""
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
            "provider": "Together AI",
            "model": self.model,
            "base_url": self.base_url,
            "api_key_set": bool(self.api_key),
        }
