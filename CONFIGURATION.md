# ZettaBrain Skills Configuration

## Environment Variables

You can configure ZettaBrain Skills using environment variables.

### Ollama Configuration

```bash
# Ollama server URL (default: http://localhost:11434)
export OLLAMA_BASE_URL="http://localhost:11434"

# Model to use (default: llama3.1:8b)
export OLLAMA_MODEL="llama3.1:8b"

# Request timeout in seconds (default: 600 = 10 minutes)
export OLLAMA_TIMEOUT="600"
```

### Quick Setup for Production

Add to your `~/.bashrc` or `~/.profile`:

```bash
# ZettaBrain Skills Configuration
export OLLAMA_TIMEOUT="900"  # 15 minutes for large documents
export OLLAMA_MODEL="llama3.1:8b"
```

Then reload:
```bash
source ~/.bashrc
```

## Timeout Configuration

### Default Timeouts

- **Default**: 600 seconds (10 minutes)
- Suitable for most quotes and documents

### Recommended Timeouts by Use Case

| Use Case | Timeout | Command |
|----------|---------|---------|
| Simple summaries (< 500 words) | 120s | `export OLLAMA_TIMEOUT=120` |
| Standard quotes | 300s | `export OLLAMA_TIMEOUT=300` |
| Complex quotes with pricing | 600s | `export OLLAMA_TIMEOUT=600` |
| Large reports (> 2000 tokens) | 900s | `export OLLAMA_TIMEOUT=900` |
| Maximum (very large docs) | 1800s | `export OLLAMA_TIMEOUT=1800` |

### Per-Command Timeout

```bash
# One-time timeout for a single command
OLLAMA_TIMEOUT=900 zbs generate skill.md --input "long text..."
```

## Model Selection

### Available Models

```bash
# List installed models
ollama list

# Use different model
export OLLAMA_MODEL="mistral:7b"     # Faster, less accurate
export OLLAMA_MODEL="llama3.1:8b"    # Balanced (default)
export OLLAMA_MODEL="llama3.1:70b"   # More accurate, slower, needs GPU
```

### Model Recommendations

| Model | Speed | Quality | RAM | Use Case |
|-------|-------|---------|-----|----------|
| `mistral:7b` | Fast | Good | 8GB | Quick summaries |
| `llama3.1:8b` | Medium | Great | 8GB | General use (default) |
| `qwen2.5:7b` | Medium | Great | 8GB | Multilingual |
| `llama3.1:70b` | Slow | Excellent | 48GB | Complex analysis |

## Troubleshooting Timeouts

### If you get timeout errors:

**Option 1: Increase timeout**
```bash
export OLLAMA_TIMEOUT=900
zbs generate skill.md --input "text"
```

**Option 2: Reduce output size**
```bash
zbs generate skill.md --input "text" --max-tokens 1000
```

**Option 3: Use faster model**
```bash
export OLLAMA_MODEL="mistral:7b"
zbs generate skill.md --input "text"
```

**Option 4: Check Ollama performance**
```bash
# Check if Ollama is running smoothly
ollama ps

# Check system resources
htop  # or top

# Restart Ollama if needed
sudo systemctl restart ollama
```

## Production Recommendations

For production use (like 3RVA):

```bash
# Add to /etc/environment or ~/.bashrc
export OLLAMA_TIMEOUT="900"          # 15 minutes
export OLLAMA_MODEL="llama3.1:8b"    # Proven model
export OLLAMA_BASE_URL="http://localhost:11434"

# Reload
source ~/.bashrc

# Verify
echo $OLLAMA_TIMEOUT
# Should output: 900
```

## Testing Your Configuration

```bash
# Test with simple generation
zbs generate examples/simple-summarizer.md --input "Test configuration"

# Test with complex quote
zbs generate examples/3rva-quote-full.md --input "Customer needs 100 lbs R-22..."

# Check what's configured
zbs check
```

## Command-Line Overrides

Environment variables can be overridden per command:

```bash
# Use different timeout just for this command
OLLAMA_TIMEOUT=1200 zbs generate skill.md --input "text"

# Use different model just for this command
OLLAMA_MODEL="mistral:7b" zbs generate skill.md --input "text"

# Combine multiple overrides
OLLAMA_TIMEOUT=900 OLLAMA_MODEL="llama3.1:70b" zbs generate skill.md --input "text"
```

## FAQ

**Q: What's the maximum timeout?**
A: No hard limit, but 1800s (30 minutes) is practical maximum. Most operations complete in 2-10 minutes.

**Q: Does increasing timeout slow down fast operations?**
A: No, timeout is maximum wait time. Fast operations still complete quickly.

**Q: Can I set permanent configuration?**
A: Yes, add exports to `~/.bashrc` or `~/.profile`:
```bash
echo 'export OLLAMA_TIMEOUT=900' >> ~/.bashrc
source ~/.bashrc
```

**Q: How do I check current configuration?**
```bash
env | grep OLLAMA
```

**Q: What if I need even longer timeouts?**
A: You can set any value:
```bash
export OLLAMA_TIMEOUT=3600  # 1 hour
```

But consider:
- Using `--max-tokens` to limit output
- Breaking large documents into smaller chunks
- Using a faster model for drafts
