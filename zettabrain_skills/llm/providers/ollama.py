"""
Ollama LLM provider implementation
"""

import httpx
from typing import Dict, Any, Iterator
from zettabrain_skills.llm.base import LLMProvider


class OllamaProvider(LLMProvider):
    """Ollama LLM provider for local model inference"""

    def __init__(
        self, base_url: str = "http://localhost:11434", model: str = "llama3.1:8b", timeout: int = 120
    ):
        """
        Initialize Ollama provider

        Args:
            base_url: Ollama server URL
            model: Model name (e.g., 'llama3.1:8b', 'mistral:7b')
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000, **kwargs
    ) -> str:
        """Generate text using Ollama"""

        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
            },
        }

        # Add any additional Ollama-specific options
        if kwargs:
            payload["options"].update(kwargs)

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
                return result.get("response", "")
        except httpx.TimeoutException:
            raise RuntimeError(
                f"Ollama generation timed out after {self.timeout}s. "
                "Try reducing max_tokens or increasing timeout."
            )
        except httpx.HTTPError as e:
            raise RuntimeError(f"Ollama HTTP error: {e}")
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {e}")

    def stream(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000, **kwargs
    ) -> Iterator[str]:
        """Stream generated text token by token"""

        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": True,
            "options": {
                "num_predict": max_tokens,
            },
        }

        if kwargs:
            payload["options"].update(kwargs)

        try:
            with httpx.Client(timeout=self.timeout) as client:
                with client.stream("POST", url, json=payload) as response:
                    response.raise_for_status()
                    for line in response.iter_lines():
                        if line:
                            import json

                            try:
                                data = json.loads(line)
                                if "response" in data:
                                    yield data["response"]
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            raise RuntimeError(f"Ollama streaming failed: {e}")

    def check_health(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    f"{self.base_url}/api/show", json={"name": self.model}
                )
                response.raise_for_status()
                info = response.json()
                return {
                    "provider": "ollama",
                    "model": self.model,
                    "base_url": self.base_url,
                    "details": info,
                }
        except Exception as e:
            return {
                "provider": "ollama",
                "model": self.model,
                "base_url": self.base_url,
                "error": str(e),
            }
