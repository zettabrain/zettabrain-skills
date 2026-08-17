"""Data models for discovery documents."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PricingRule(BaseModel):
    """Pricing rule extracted from discovery document."""

    item_name: str
    unit_price: float
    unit: str = "each"
    markup_percent: Optional[float] = None
    minimum_quantity: Optional[int] = None
    notes: Optional[str] = None


class ServiceItem(BaseModel):
    """Service or product offering."""

    name: str
    description: str
    category: Optional[str] = None
    pricing: Optional[PricingRule] = None
    available: bool = True


class BusinessInfo(BaseModel):
    """Structured business information from discovery document."""

    company_name: str
    industry: str
    description: Optional[str] = None

    # Contact information
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None

    # Business data
    services: List[ServiceItem] = Field(default_factory=list)
    pricing_rules: List[PricingRule] = Field(default_factory=list)

    # Policies
    payment_terms: Optional[str] = None
    warranty_policy: Optional[str] = None
    service_area: Optional[str] = None

    # Metadata
    raw_content: Optional[str] = None
    extraction_notes: List[str] = Field(default_factory=list)

    def to_skill_context(self) -> str:
        """Convert business info to skill context string."""
        context_parts = [
            f"# Business Context: {self.company_name}",
            f"Industry: {self.industry}",
        ]

        if self.description:
            context_parts.append(f"\n{self.description}")

        if self.contact_phone:
            context_parts.append(f"\nPhone: {self.contact_phone}")
        if self.contact_email:
            context_parts.append(f"Email: {self.contact_email}")
        if self.address:
            context_parts.append(f"Address: {self.address}")

        if self.services:
            context_parts.append("\n## Available Services/Products:")
            for service in self.services:
                context_parts.append(f"- {service.name}: {service.description}")
                if service.pricing:
                    context_parts.append(f"  Price: ${service.pricing.unit_price}/{service.pricing.unit}")

        if self.pricing_rules:
            context_parts.append("\n## Pricing Rules:")
            for rule in self.pricing_rules:
                rule_str = f"- {rule.item_name}: ${rule.unit_price}/{rule.unit}"
                if rule.markup_percent:
                    rule_str += f" (markup: {rule.markup_percent}%)"
                if rule.notes:
                    rule_str += f" - {rule.notes}"
                context_parts.append(rule_str)

        if self.payment_terms:
            context_parts.append(f"\n## Payment Terms:\n{self.payment_terms}")

        if self.warranty_policy:
            context_parts.append(f"\n## Warranty Policy:\n{self.warranty_policy}")

        if self.service_area:
            context_parts.append(f"\n## Service Area:\n{self.service_area}")

        return "\n".join(context_parts)
