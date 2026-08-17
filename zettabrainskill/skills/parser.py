"""
Skill parser - Parse YAML frontmatter + markdown skill files
"""

import frontmatter
from pathlib import Path
from typing import Dict, Any
from zettabrainskill.core.models import Skill


class SkillParser:
    """Parse skill files (YAML frontmatter + markdown)"""

    @staticmethod
    def parse_file(file_path: str | Path) -> Skill:
        """
        Parse a skill file

        Args:
            file_path: Path to skill file (.md with YAML frontmatter)

        Returns:
            Parsed Skill object

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If required fields are missing or invalid
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Skill file not found: {file_path}")

        # Parse frontmatter and content
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Extract metadata from frontmatter
        metadata = post.metadata
        instructions = post.content

        # Validate required fields
        required_fields = ["name", "version", "description"]
        for field in required_fields:
            if not metadata.get(field):
                raise ValueError(f"Skill must have '{field}' field in frontmatter")

        # Validate instructions not empty
        if not instructions or len(instructions.strip()) < 50:
            raise ValueError("Skill instructions must be at least 50 characters")

        # Build Skill object with all fields
        skill_data = {
            "name": metadata["name"],
            "version": metadata["version"],
            "description": metadata["description"],
            "instructions": instructions,
        }

        # Add optional fields if present
        optional_fields = [
            "business_type",
            "author",
            "created_at",
            "updated_at",
            "requires_corpus",
            "requires_discovery",
            "inputs",
            "outputs",
            "references",
            "temperature",
            "max_tokens",
            "citation_required",
            "escalation_triggers",
            "tags",
            "deprecated",
        ]

        for field in optional_fields:
            if field in metadata:
                skill_data[field] = metadata[field]

        skill = Skill(**skill_data)

        return skill

    @staticmethod
    def validate(skill: Skill) -> tuple[bool, list[str]]:
        """
        Validate a skill

        Args:
            skill: Skill object to validate

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        # Check instructions length
        if len(skill.instructions) < 50:
            errors.append("Skill instructions too short (minimum 50 characters)")

        # Check for placeholder text
        placeholders = ["<<FILL", "TODO", "FIXME", "TEMPLATE"]
        for placeholder in placeholders:
            if placeholder in skill.instructions:
                errors.append(f"Skill contains placeholder text: {placeholder}")

        # Check version format (semantic versioning)
        version_parts = skill.version.split(".")
        if len(version_parts) != 3:
            errors.append(
                f"Version must be semantic (MAJOR.MINOR.PATCH), got: {skill.version}"
            )

        # Check temperature range
        if not 0.0 <= skill.temperature <= 2.0:
            errors.append(f"Temperature must be between 0.0 and 2.0, got: {skill.temperature}")

        # Check max_tokens positive
        if skill.max_tokens <= 0:
            errors.append(f"max_tokens must be positive, got: {skill.max_tokens}")

        return (len(errors) == 0, errors)

    @staticmethod
    def parse_and_validate(file_path: str | Path) -> Skill:
        """
        Convenience method to parse and validate in one call

        Args:
            file_path: Path to skill file

        Returns:
            Validated Skill object

        Raises:
            ValueError: If parsing or validation fails
        """
        skill = SkillParser.parse_file(file_path)
        is_valid, errors = SkillParser.validate(skill)

        if not is_valid:
            error_msg = "Skill validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ValueError(error_msg)

        return skill


def load_skill(file_path: str | Path) -> Skill:
    """
    Convenience function to load and validate a skill

    Args:
        file_path: Path to skill file

    Returns:
        Validated Skill object
    """
    return SkillParser.parse_and_validate(file_path)
