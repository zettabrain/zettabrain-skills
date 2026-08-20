"""
Document generation engine - Core orchestration logic
"""

import uuid
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from zettabrain_skills.core.models import Skill, GenerationRequest, GenerationResult
from zettabrain_skills.llm.base import LLMProvider
from zettabrain_skills.llm.factory import create_llm_provider


class GenerationEngine:
    """Core document generation engine"""

    def __init__(
        self,
        llm_provider: Optional[LLMProvider] = None,
        corpus_retriever=None,
    ):
        """
        Initialize generation engine

        Args:
            llm_provider: LLM provider instance (defaults to configured provider)
            corpus_retriever: Optional CorpusRetriever for corpus-grounded generation
        """
        self.llm_provider = llm_provider or create_llm_provider()
        self._corpus_retriever = corpus_retriever

    @property
    def corpus_retriever(self):
        return self._corpus_retriever

    @corpus_retriever.setter
    def corpus_retriever(self, retriever):
        self._corpus_retriever = retriever

    def build_prompt(
        self,
        skill: Skill,
        user_input: str,
        context: Optional[Dict[str, Any]] = None,
        corpus_context: Optional[str] = None,
    ) -> str:
        """
        Build prompt from skill instructions + user input + context

        Args:
            skill: Skill to execute
            user_input: User's request/input
            context: Additional context (discovery data, etc.)
            corpus_context: Pre-formatted corpus retrieval context

        Returns:
            Complete prompt for LLM
        """
        prompt_parts = []

        # System context
        prompt_parts.append("You are an AI assistant that follows instructions precisely.")
        prompt_parts.append(
            "Your task is to generate a document based on the instructions below."
        )
        prompt_parts.append("")

        # Skill instructions
        prompt_parts.append("# TASK INSTRUCTIONS")
        prompt_parts.append(skill.instructions)
        prompt_parts.append("")

        # Corpus context (from vector retrieval)
        if corpus_context:
            prompt_parts.append(corpus_context)
            prompt_parts.append("")

        # Context from discovery or other sources
        if context:
            prompt_parts.append("# CONTEXT")
            prompt_parts.append(
                "The following context information should inform your response:"
            )
            prompt_parts.append("")

            for key, value in context.items():
                prompt_parts.append(f"## {key}")
                prompt_parts.append(str(value))
                prompt_parts.append("")

        # User input
        prompt_parts.append("# USER REQUEST")
        prompt_parts.append(user_input)
        prompt_parts.append("")

        # Output instructions
        prompt_parts.append("# OUTPUT INSTRUCTIONS")
        prompt_parts.append("Generate the requested document following the task instructions above.")

        if skill.citation_required:
            prompt_parts.append(
                "IMPORTANT: Include citations to source documents where applicable. "
                "Reference the source title and reference number for each claim."
            )

        if corpus_context and not skill.citation_required:
            prompt_parts.append(
                "When using information from the corpus context above, "
                "note the source document title."
            )

        prompt_parts.append("")
        prompt_parts.append("Begin your response now:")

        return "\n".join(prompt_parts)

    def generate(self, skill: Skill, request: GenerationRequest) -> GenerationResult:
        """
        Generate a document using a skill

        Args:
            skill: Skill to execute
            request: Generation request with input and context

        Returns:
            GenerationResult with generated content or error
        """
        start_time = time.time()

        try:
            # Retrieve corpus context if skill requires it
            corpus_context = None
            citations: List[str] = []

            if skill.requires_corpus and self._corpus_retriever:
                corpus_text, citation_objects = (
                    self._corpus_retriever.get_context_for_generation(
                        query=request.input,
                        n_results=5,
                        min_relevance=0.3,
                    )
                )
                if corpus_text:
                    corpus_context = corpus_text
                    citations = [
                        f"{c.document_title}"
                        + (f" ({c.citation_ref})" if c.citation_ref else "")
                        for c in citation_objects
                    ]

            # Build prompt
            prompt = self.build_prompt(
                skill, request.input, request.context, corpus_context
            )

            # Use request overrides or skill defaults
            temperature = request.temperature if request.temperature is not None else skill.temperature
            max_tokens = request.max_tokens if request.max_tokens is not None else skill.max_tokens

            # Generate with LLM
            content = self.llm_provider.generate(
                prompt=prompt, temperature=temperature, max_tokens=max_tokens
            )

            # Calculate generation time
            generation_time_ms = int((time.time() - start_time) * 1000)

            # Create result
            result = GenerationResult(
                id=str(uuid.uuid4()),
                skill_name=skill.name,
                skill_version=skill.version,
                content=content,
                metadata={
                    "business_id": request.business_id,
                    "input": request.input,
                    "context_keys": list(request.context.keys()) if request.context else [],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "model": getattr(self.llm_provider, "model", "unknown"),
                    "corpus_used": corpus_context is not None,
                },
                created_at=datetime.now(),
                success=True,
                generation_time_ms=generation_time_ms,
                citations=citations,
            )

            return result

        except Exception as e:
            generation_time_ms = int((time.time() - start_time) * 1000)

            return GenerationResult(
                id=str(uuid.uuid4()),
                skill_name=skill.name,
                skill_version=skill.version,
                content="",
                metadata={
                    "business_id": request.business_id,
                    "input": request.input,
                },
                success=False,
                error=str(e),
                generation_time_ms=generation_time_ms,
            )

    def validate_output(self, skill: Skill, result: GenerationResult) -> tuple[bool, list[str]]:
        """
        Validate generated output

        Args:
            skill: Skill that was executed
            result: Generation result

        Returns:
            (is_valid, list_of_warnings)
        """
        warnings = []

        if not result.success:
            return (False, ["Generation failed"])

        # Check if output is empty
        if not result.content or len(result.content.strip()) == 0:
            warnings.append("Generated content is empty")

        # Check if citations are required but missing
        if skill.citation_required:
            # Simple citation detection (look for common citation patterns)
            citation_patterns = ["Source:", "Citation:", "Reference:", "[", "http://", "https://"]
            has_citation = any(pattern in result.content for pattern in citation_patterns)

            if not has_citation:
                warnings.append(
                    "Skill requires citations but none found in output"
                )

        # Check if output is suspiciously short
        if len(result.content) < 50:
            warnings.append("Generated content is very short (< 50 characters)")

        return (len(warnings) == 0, warnings)
