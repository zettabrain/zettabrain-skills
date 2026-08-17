"""
Setup script for ZettaBrainSkill
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="zettabrain-skills",
    version="0.2.0",
    author="ZettaBrain",
    author_email="hello@zettabrain.com",
    description="Open-source skill-based document generation platform with AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zettabrain/zettabrain-skills",
    project_urls={
        "Bug Tracker": "https://github.com/zettabrain/zettabrain-skills/issues",
        "Documentation": "https://github.com/zettabrain/zettabrain-skills",
        "Source Code": "https://github.com/zettabrain/zettabrain-skills",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.104.0",
        "typer[all]==0.9.0",
        "pydantic>=2.5.0",
        "pyyaml>=6.0",
        "httpx>=0.25.2",
        "python-multipart>=0.0.6",
        "uvicorn[standard]>=0.24.0",
        "python-frontmatter>=1.1.0",
        "rich>=13.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.11.0",
            "ruff>=0.1.6",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "zbs=zettabrain_skills.cli.main:app",
            "zettabrain-skills=zettabrain_skills.cli.main:app",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="ai llm document-generation automation skills nlp",
)
