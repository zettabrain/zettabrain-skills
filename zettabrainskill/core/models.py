"""
Core data models for ZettaBrainSkill
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class Skill(BaseModel):
    """A skill definition that tells the AI how to perform a task"""

    name: str
    version: str
    description: str
    business_type: str = "generic"
    author: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    # Dependencies
    requires_corpus: bool = False
    requires_discovery: List[str] = Field(default_factory=list)

    # Input/Output
    inputs: List[str] | Dict[str, Any] = Field(default_factory=list)
    outputs: List[str] | Dict[str, Any] = Field(default_factory=list)

    # References (loaded on-demand)
    references: Dict[str, str] = Field(default_factory=dict)

    # Instructions (markdown body)
    instructions: str

    # Behavior
    temperature: float = 0.7
    max_tokens: int = 2000
    citation_required: bool = False
    escalation_triggers: List[str] = Field(default_factory=list)

    # Metadata
    tags: List[str] = Field(default_factory=list)
    deprecated: bool = False

    class Config:
        frozen = False


class GenerationRequest(BaseModel):
    """Request to generate a document"""

    input: str
    skill_name: Optional[str] = None
    business_id: str = "default"
    context: Dict[str, Any] = Field(default_factory=dict)

    # Override skill parameters
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class GenerationResult(BaseModel):
    """Result of document generation"""

    id: str
    skill_name: str
    skill_version: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: str = "system"
    success: bool = True
    error: Optional[str] = None
    citations: List[str] = Field(default_factory=list)

    # Performance metrics
    generation_time_ms: Optional[int] = None
    tokens_used: Optional[int] = None


class Business(BaseModel):
    """Business/tenant configuration"""

    id: str
    name: str
    business_type: str  # service, manufacturing, consulting, etc.
    created_at: datetime = Field(default_factory=datetime.now)

    # Paths
    skills_path: Optional[str] = None
    corpus_path: Optional[str] = None
    discovery_path: Optional[str] = None

    # Settings
    settings: Dict[str, Any] = Field(default_factory=dict)
    active: bool = True


class DiscoveryData(BaseModel):
    """Extracted business logic from discovery process"""

    business_id: str
    section: str  # pricing-rules, workflows, escalation-rules, etc.
    data: Dict[str, Any]
    version: str = "1.0"
    updated_at: datetime = Field(default_factory=datetime.now)
