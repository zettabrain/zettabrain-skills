"""
Tests for skill parser
"""

import pytest
from pathlib import Path
from zettabrain_skills.skills.parser import SkillParser, load_skill
from zettabrain_skills.core.models import Skill


def test_parse_valid_skill(tmp_path):
    """Test parsing a valid skill file"""
    skill_content = """---
name: test-skill
version: 1.0.0
description: A test skill for unit testing
business_type: generic
temperature: 0.5
max_tokens: 1000
---

# Test Skill

This is a test skill with enough content to pass validation.
It has multiple lines and provides clear instructions for the AI.
"""

    skill_file = tmp_path / "test-skill.md"
    skill_file.write_text(skill_content)

    skill = SkillParser.parse_file(skill_file)

    assert skill.name == "test-skill"
    assert skill.version == "1.0.0"
    assert skill.description == "A test skill for unit testing"
    assert skill.business_type == "generic"
    assert skill.temperature == 0.5
    assert skill.max_tokens == 1000
    assert "Test Skill" in skill.instructions


def test_parse_missing_name(tmp_path):
    """Test that missing required field raises error"""
    skill_content = """---
version: 1.0.0
description: Missing name field
---

# Instructions
Test instructions here with enough content.
"""

    skill_file = tmp_path / "bad-skill.md"
    skill_file.write_text(skill_content)

    with pytest.raises(ValueError, match="must have 'name' field"):
        SkillParser.parse_file(skill_file)


def test_validate_short_instructions():
    """Test validation catches short instructions"""
    skill = Skill(
        name="test",
        version="1.0.0",
        description="Test",
        instructions="Too short",
    )

    is_valid, errors = SkillParser.validate(skill)

    assert not is_valid
    assert any("too short" in e.lower() for e in errors)


def test_validate_placeholder_text():
    """Test validation catches placeholder text"""
    skill = Skill(
        name="test",
        version="1.0.0",
        description="Test",
        instructions="This has <<FILL>> placeholder text that should be caught by validation.",
    )

    is_valid, errors = SkillParser.validate(skill)

    assert not is_valid
    assert any("placeholder" in e.lower() for e in errors)


def test_validate_invalid_version():
    """Test validation catches invalid version format"""
    skill = Skill(
        name="test",
        version="1.0",  # Should be MAJOR.MINOR.PATCH
        description="Test",
        instructions="Valid instructions with enough content to pass length check.",
    )

    is_valid, errors = SkillParser.validate(skill)

    assert not is_valid
    assert any("semantic" in e.lower() for e in errors)


def test_validate_valid_skill():
    """Test validation passes for valid skill"""
    skill = Skill(
        name="test",
        version="1.0.0",
        description="Test skill",
        instructions="This is a valid skill with proper instructions that are long enough.",
        temperature=0.7,
        max_tokens=2000,
    )

    is_valid, errors = SkillParser.validate(skill)

    assert is_valid
    assert len(errors) == 0
