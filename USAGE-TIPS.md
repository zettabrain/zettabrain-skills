# ZettaBrain Skills - Usage Tips

## Common Issues and Solutions

### 1. Input Text Must Be Quoted

**Error**:
```
UsageError: Got unexpected extra argument (...)
```

**Solution**: Always quote your input text with `--input`:

✅ **Correct**:
```bash
zbs generate skill.md --input "Your text here with spaces"
```

❌ **Incorrect**:
```bash
zbs generate skill.md --input Your text here  # ERROR!
```

### 2. Example Commands

#### Simple Summarization
```bash
zbs generate examples/simple-summarizer.md \
  --input "Artificial intelligence is transforming business operations. Companies use AI for customer service automation, predictive analytics, and process optimization."
```

#### With Output File
```bash
zbs generate examples/simple-summarizer.md \
  --input "Your long text here..." \
  --output summary.md
```

#### Custom Parameters
```bash
zbs generate examples/simple-summarizer.md \
  --input "Text to summarize" \
  --temperature 0.5 \
  --max-tokens 300
```

#### Quote Generation
```bash
zbs generate examples/3rva-quote-simple.md \
  --input "Customer needs 100 lbs R-22 delivered to Richmond, VA by Friday"
```

### 3. Multi-line Input

For longer text, use quotes with escaped newlines:

```bash
zbs generate skill.md --input "First paragraph.

Second paragraph with more text.

Third paragraph here."
```

Or use a file:
```bash
cat input.txt | xargs -0 zbs generate skill.md --input
```

### 4. Python 3.14 Compatibility

If you see:
```
TypeError: TyperArgument.make_metavar() takes 1 positional argument but 2 were given
```

**Solution**: Update to latest version:
```bash
pipx uninstall zettabrain-skills
pipx install git+https://github.com/zettabrain/zettabrain-skills.git
```

Version 0.1.3+ includes Python 3.14 compatibility.

## Command Reference

### Generate Document
```bash
zbs generate <skill-file> --input "text" [OPTIONS]

Options:
  --input, -i TEXT        Input text (REQUIRED, must be quoted)
  --output, -o PATH       Output file path
  --temperature, -t FLOAT Temperature (0.0-2.0)
  --max-tokens, -m INT    Max output length
  --business, -b TEXT     Business ID
```

### Validate Skill
```bash
zbs validate <skill-file>
```

### Check Ollama Status
```bash
zbs check
```

### Show Version
```bash
zbs version
```

## Working Examples

### 1. Text Summarization
```bash
zbs generate examples/simple-summarizer.md \
  --input "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing computer programs that can access data and use it to learn for themselves. The process begins with observations or data, such as examples, direct experience, or instruction, in order to look for patterns in data and make better decisions in the future."
```

**Expected Output**: 3-5 bullet point summary

### 2. Service Quote
```bash
zbs generate examples/3rva-quote-simple.md \
  --input "Need quote for refrigerant recovery job. Site: commercial building in downtown Richmond. System type: R-410A chiller, approximately 200 lbs. Need service next week."
```

**Expected Output**: Structured quote with scope, pricing notes, and missing information

### 3. Save to File
```bash
zbs generate examples/simple-summarizer.md \
  --input "Your text to summarize..." \
  --output result.md

# View the result
cat result.md
```

### 4. Adjust Creativity
```bash
# More deterministic (factual, consistent)
zbs generate skill.md --input "..." --temperature 0.2

# More creative (varied, exploratory)
zbs generate skill.md --input "..." --temperature 0.9
```

### 5. Control Output Length
```bash
# Shorter output
zbs generate skill.md --input "..." --max-tokens 300

# Longer output
zbs generate skill.md --input "..." --max-tokens 2000
```

## Troubleshooting

### Ollama Not Running
```bash
# Check status
zbs check

# If not running:
ollama serve &

# Pull model if needed
ollama pull llama3.1:8b
```

### Slow Generation
```bash
# Use smaller model
ollama pull mistral:7b

# Set it as default
export OLLAMA_MODEL=mistral:7b

# Or reduce output length
zbs generate skill.md --input "..." --max-tokens 500
```

### Skill Validation Fails
```bash
# Check the skill file
zbs validate my-skill.md

# Common issues:
# - Missing required fields (name, version, description)
# - Instructions too short (< 50 characters)
# - Invalid version format (must be MAJOR.MINOR.PATCH)
```

## Shell Tips

### Bash/Zsh Aliases
Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Shorthand for common operations
alias zbsv='zbs version'
alias zbsc='zbs check'
alias zbsg='zbs generate'

# Quick summarize
summarize() {
  zbs generate examples/simple-summarizer.md --input "$1"
}

# Usage: summarize "Your text here"
```

### Using with Pipes
```bash
# Summarize a file
cat document.txt | xargs -I {} zbs generate examples/simple-summarizer.md --input "{}"

# Summarize clipboard (macOS)
pbpaste | xargs -I {} zbs generate examples/simple-summarizer.md --input "{}"

# Summarize clipboard (Linux with xclip)
xclip -o | xargs -I {} zbs generate examples/simple-summarizer.md --input "{}"
```

## Best Practices

1. **Always quote input**: Use double quotes for `--input`
2. **Validate skills first**: Run `zbs validate` before using new skills
3. **Check Ollama**: Run `zbs check` before generating
4. **Save important outputs**: Use `--output` to save to files
5. **Start simple**: Test with short inputs before long documents
6. **Adjust temperature**: Lower for factual, higher for creative
7. **Use appropriate models**: Smaller models are faster, larger are better

## Getting Help

```bash
# Command help
zbs --help
zbs generate --help

# Check system
zbs check

# Validate skill
zbs validate skill.md
```

## Links

- [Installation Guide](INSTALL-UBUNTU.md)
- [Quick Reference](QUICKREF.md)
- [Setup Guide](SETUP.md)
- [Repository](https://github.com/zettabrain/zettabrain-skills)
