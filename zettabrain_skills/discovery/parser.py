"""Discovery document parser using LLM for extraction."""

import json
import re
from pathlib import Path
from typing import Optional, Dict, Any

import httpx
from rich.console import Console

from .models import BusinessInfo, PricingRule, ServiceItem


console = Console()


EXTRACTION_PROMPT = """You are a business information extraction assistant. Extract structured information from the discovery document below.

**Discovery Document:**
{document_content}

**Extract the following information in JSON format:**

{{
  "company_name": "Company name",
  "industry": "Industry/sector",
  "description": "Brief company description",
  "contact_email": "Email if found",
  "contact_phone": "Phone if found",
  "address": "Address if found",
  "website": "Website if found",
  "services": [
    {{
      "name": "Service/product name",
      "description": "What it is",
      "category": "Category if applicable"
    }}
  ],
  "pricing_rules": [
    {{
      "item_name": "Item name",
      "unit_price": 0.00,
      "unit": "each/lb/cylinder/hour",
      "markup_percent": 0,
      "notes": "Any pricing notes"
    }}
  ],
  "payment_terms": "Payment terms if mentioned",
  "warranty_policy": "Warranty info if mentioned",
  "service_area": "Service area if mentioned",
  "extraction_notes": ["Any notes about extraction quality or missing info"]
}}

**Important:**
- Extract ALL services and pricing information
- Use exact numbers for prices (no ranges unless necessary)
- If information is missing, use null
- Be thorough - this data will be used to generate business documents

Return ONLY valid JSON, no additional text.
"""


class DiscoveryParser:
    """Parse discovery documents and extract business information."""

    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        model: str = "llama3.1:8b",
        timeout: int = 300,
    ):
        self.ollama_url = ollama_url
        self.model = model
        self.timeout = timeout

    def parse_document(self, document_path: Path) -> BusinessInfo:
        """Parse a discovery document and return structured business info.

        Args:
            document_path: Path to the discovery document (markdown, txt, etc.)

        Returns:
            BusinessInfo object with extracted data
        """
        # Read document content
        document_content = document_path.read_text()

        # Build extraction prompt
        prompt = EXTRACTION_PROMPT.format(document_content=document_content)

        console.print(f"[blue]Extracting business info from {document_path.name}...[/blue]")

        # Call LLM for extraction
        extracted_json = self._call_llm(prompt)

        # Parse JSON response
        try:
            data = json.loads(extracted_json)
        except json.JSONDecodeError as e:
            # Try to extract JSON from response if it has extra text
            json_match = re.search(r'\{.*\}', extracted_json, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                console.print(f"[red]Failed to parse JSON response: {e}[/red]")
                raise ValueError(f"Could not parse LLM response as JSON: {extracted_json[:200]}")

        # Convert to BusinessInfo model
        business_info = self._dict_to_business_info(data)
        business_info.raw_content = document_content

        console.print(f"[green]✓ Extracted info for {business_info.company_name}[/green]")
        console.print(f"  Services: {len(business_info.services)}")
        console.print(f"  Pricing rules: {len(business_info.pricing_rules)}")

        return business_info

    def _call_llm(self, prompt: str) -> str:
        """Call Ollama API for extraction."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,  # Low temperature for structured extraction
                            "num_predict": 2000,
                        },
                    },
                )
                response.raise_for_status()
                result = response.json()
                return result.get("response", "")

        except httpx.TimeoutException:
            raise Exception(f"LLM request timed out after {self.timeout}s")
        except httpx.HTTPError as e:
            raise Exception(f"LLM request failed: {e}")

    def _dict_to_business_info(self, data: Dict[str, Any]) -> BusinessInfo:
        """Convert extracted dict to BusinessInfo model."""
        # Convert services
        services = []
        for s in data.get("services", []):
            service = ServiceItem(
                name=s.get("name", ""),
                description=s.get("description", ""),
                category=s.get("category"),
            )
            services.append(service)

        # Convert pricing rules
        pricing_rules = []
        for p in data.get("pricing_rules", []):
            if p.get("item_name") and p.get("unit_price"):
                rule = PricingRule(
                    item_name=p["item_name"],
                    unit_price=float(p["unit_price"]),
                    unit=p.get("unit", "each"),
                    markup_percent=float(p["markup_percent"]) if p.get("markup_percent") else None,
                    notes=p.get("notes"),
                )
                pricing_rules.append(rule)

        return BusinessInfo(
            company_name=data.get("company_name", "Unknown"),
            industry=data.get("industry", "Unknown"),
            description=data.get("description"),
            contact_email=data.get("contact_email"),
            contact_phone=data.get("contact_phone"),
            address=data.get("address"),
            website=data.get("website"),
            services=services,
            pricing_rules=pricing_rules,
            payment_terms=data.get("payment_terms"),
            warranty_policy=data.get("warranty_policy"),
            service_area=data.get("service_area"),
            extraction_notes=data.get("extraction_notes", []),
        )

    def save_business_info(self, business_info: BusinessInfo, output_path: Path) -> None:
        """Save business info as JSON for later use."""
        output_path.write_text(business_info.model_dump_json(indent=2))
        console.print(f"[green]✓ Saved business info to {output_path}[/green]")

    def load_business_info(self, info_path: Path) -> BusinessInfo:
        """Load previously extracted business info."""
        data = json.loads(info_path.read_text())
        return BusinessInfo(**data)
