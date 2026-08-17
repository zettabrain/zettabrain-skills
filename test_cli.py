#!/usr/bin/env python3
"""
Test CLI locally without installing
"""

import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))

from zettabrain_skills.cli.main import app

if __name__ == "__main__":
    app()
