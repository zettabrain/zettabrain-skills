# Upgrade ZettaBrain Skills

## Force Reinstall (Fixes Python 3.14 Issue)

```bash
# 1. Uninstall completely
pipx uninstall zettabrain-skills

# 2. Clear pip cache (important!)
pip cache purge

# 3. Reinstall latest version
pipx install --force git+https://github.com/zettabrain/zettabrain-skills.git

# 4. Verify version includes typer 0.12+
pipx runpip zettabrain-skills list | grep typer
# Should show: typer >= 0.12.0

# 5. Test it works
zbs version
zbs check
```

## If Still Having Issues

Try installing with verbose output to see what's happening:

```bash
# Uninstall
pipx uninstall zettabrain-skills

# Install with verbose
pipx install --verbose git+https://github.com/zettabrain/zettabrain-skills.git

# Check installed packages
pipx runpip zettabrain-skills list
```

## Verify Correct Version

After installation, check:

```bash
# Should output: ZettaBrain Skills version 0.1.0
zbs version

# Check typer version (should be >= 0.12.0)
pipx runpip zettabrain-skills show typer

# Should work without error
zbs check
```

## Test Generation

```bash
# This should work now (with quotes)
zbs generate examples/simple-summarizer.md \
  --input "Artificial intelligence is transforming business operations"
```

## Alternative: Install from Specific Commit

If the above doesn't work, try installing from the latest commit:

```bash
pipx uninstall zettabrain-skills

pipx install git+https://github.com/zettabrain/zettabrain-skills.git@main

# Or specific commit
pipx install git+https://github.com/zettabrain/zettabrain-skills.git@0b31168
```

## Check What You Have Installed

```bash
# Show all installed packages in zettabrain-skills environment
pipx runpip zettabrain-skills list

# Look for:
# - typer >= 0.12.0  (REQUIRED for Python 3.14)
# - rich >= 13.7.0
# - pydantic >= 2.5.0
```

## Nuclear Option: Fresh Install

If nothing works, do a complete clean install:

```bash
# 1. Remove everything
pipx uninstall zettabrain-skills
rm -rf ~/.local/pipx/venvs/zettabrain-skills
pip cache purge

# 2. Update pipx itself
python3 -m pip install --upgrade pipx

# 3. Fresh install
pipx install git+https://github.com/zettabrain/zettabrain-skills.git

# 4. Verify
zbs --version
```
