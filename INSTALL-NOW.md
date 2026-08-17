# Install v0.1.6 - Latest Fix

## Quick Install

```bash
pipx uninstall zettabrain-skills
pipx install git+https://github.com/zettabrain/zettabrain-skills.git

zbs version
# Should show: ZettaBrainSkill version 0.1.6
```

## Test It

```bash
# Check Ollama
zbs check

# Generate (MUST quote the input!)
zbs generate examples/simple-summarizer.md --input "AI is transforming business"
```

## What Changed in v0.1.6

Removed ALL parameters from `typer.Argument()` and `typer.Option()`:

```python
# v0.1.6 - Bare minimum
skill_file: Annotated[str, typer.Argument()],
input: Annotated[str, typer.Option()],
```

This eliminates all typer parameter processing that could cause `make_metavar()` errors.

## Important

**ALWAYS quote your input text:**

```bash
# ✓ Good
zbs generate skill.md --input "Your text here"

# ✗ Bad (will split on spaces)
zbs generate skill.md --input Your text here
```
