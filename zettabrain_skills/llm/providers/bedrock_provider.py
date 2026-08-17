"""
AWS Bedrock Provider - Enterprise-grade managed inference
https://aws.amazon.com/bedrock/
"""

import os
import json
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError
from rich.console import Console

console = Console()


class BedrockProvider:
    """AWS Bedrock provider for managed LLM inference"""

    def __init__(
        self,
        model_id: str = "meta.llama3-1-8b-instruct-v1:0",
        region: str = "us-east-1",
        timeout: int = 60,
    ):
        """
        Initialize Bedrock provider

        Requires AWS credentials configured via:
        - Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        - AWS credentials file (~/.aws/credentials)
        - IAM role (if running on EC2)
        """
        self.model_id = model_id
        self.region = region
        self.timeout = timeout

        try:
            self.client = boto3.client(
                service_name="bedrock-runtime",
                region_name=region,
            )
        except Exception as e:
            raise ValueError(f"Failed to initialize Bedrock client: {e}")

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate text using AWS Bedrock"""

        try:
            # Format depends on model
            if "llama" in self.model_id.lower():
                body = json.dumps({
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_gen_len": max_tokens,
                    "top_p": kwargs.get("top_p", 0.9),
                })
            elif "claude" in self.model_id.lower():
                body = json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                })
            else:
                # Generic format
                body = json.dumps({
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "temperature": temperature,
                        "maxTokenCount": max_tokens,
                    }
                })

            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body,
            )

            response_body = json.loads(response["body"].read())

            # Extract content based on model
            if "llama" in self.model_id.lower():
                content = response_body.get("generation", "")
            elif "claude" in self.model_id.lower():
                content = response_body["content"][0]["text"]
            else:
                content = response_body.get("results", [{}])[0].get("outputText", "")

            return {
                "content": content,
                "model": self.model_id,
                "tokens_used": response_body.get("usage", {}).get("total_tokens", 0),
                "provider": "bedrock",
            }

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "AccessDeniedException":
                raise Exception(
                    "AWS Bedrock access denied. Check IAM permissions and model access."
                )
            elif error_code == "ThrottlingException":
                raise Exception(
                    "AWS Bedrock throttling. Increase quotas or reduce request rate."
                )
            else:
                raise Exception(f"Bedrock API error: {e}")

        except Exception as e:
            raise Exception(f"Bedrock generation failed: {e}")

    def check_health(self) -> bool:
        """Check if Bedrock is accessible"""
        try:
            # Try to list models as health check
            self.client.list_foundation_models()
            return True
        except Exception:
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about current model configuration"""
        return {
            "provider": "AWS Bedrock",
            "model": self.model_id,
            "region": self.region,
            "client_configured": bool(self.client),
        }


# Available Bedrock models for Llama
BEDROCK_LLAMA_MODELS = {
    "meta.llama3-1-8b-instruct-v1:0": "Llama 3.1 8B Instruct",
    "meta.llama3-1-70b-instruct-v1:0": "Llama 3.1 70B Instruct",
    "meta.llama3-1-405b-instruct-v1:0": "Llama 3.1 405B Instruct",
}
