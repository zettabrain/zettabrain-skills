# LLM Provider Options for ZettaBrain Skills

ZettaBrain Skills now supports multiple LLM providers. Choose based on your needs: speed, cost, privacy, or simplicity.

## Quick Comparison

| Provider | Speed | Cost/Doc | Setup | Best For |
|----------|-------|----------|-------|----------|
| **Groq** ⭐ | 5-10s | $0.0004 | API key | **Production (Recommended)** |
| **Together AI** | 10-15s | $0.0006 | API key | Production |
| **Ollama** | 20s GPU / 600s CPU | $0 | Local install | Development / Privacy |
| **AWS Bedrock** | 15-20s | $0.0015 | AWS account | Enterprise |
| **Claude API** | 5-10s | $0.03 | API key | Highest quality |

**Recommendation for Mike:** Use **Groq** - fastest, cheapest, simplest setup.

---

## Option 1: Groq (Recommended) ⭐

**Best for:** Production deployment, customers without GPU

### Why Groq?
- ✅ **Ultra Fast:** 5-10 seconds per document (500-800 tokens/second)
- ✅ **Cheapest:** $0.0004 per document = $0.04 for 100 documents
- ✅ **Free Tier:** 14,400 requests/day during beta
- ✅ **Simple Setup:** Just API key, no infrastructure
- ✅ **Open Source Models:** Llama 3.1, Mixtral, Gemma

### Setup

**1. Get API Key:**
```bash
# Sign up at https://console.groq.com
# Free tier: 30 requests/min, 14,400/day
# Paid: $0.05-0.10 per 1M tokens
```

**2. Configure:**
```bash
# Set environment variable
export GROQ_API_KEY="gsk_xxxxxxxxxxxxx"
export LLM_PROVIDER="groq"
```

**3. Test:**
```bash
# Start web app
./start-web.sh

# Or test CLI
zbs generate examples/3rva-quote-full.md --input "Need 100 lbs R-410A"
```

**Done!** Documents now generate in 5-10 seconds.

### Cost Calculator

| Usage | Cost/Month | Groq Tier |
|-------|------------|-----------|
| 100 docs | $0.04 | Free ✅ |
| 500 docs | $0.20 | Free ✅ |
| 1,000 docs | $0.40 | Free ✅ |
| 5,000 docs | $2.00 | Free ✅ |
| 10,000 docs | $4.00 | Paid ($0.33/day) |

**Pricing Model for Mike:**
- Charge: $99/month
- Cost: $0.04 for 100 docs
- **Profit: $98.96/month (99.96% margin)** 🎯

---

## Option 2: Together AI

**Best for:** Alternative to Groq, similar performance

### Why Together AI?
- ✅ Fast: 10-15 seconds per document
- ✅ Cheap: $0.18 per 1M tokens
- ✅ Reliable: Good uptime
- ✅ Many Models: Llama, Mixtral, Qwen, etc.

### Setup

**1. Get API Key:**
```bash
# Sign up at https://together.ai
# $25 free credits on signup
```

**2. Configure:**
```bash
export TOGETHER_API_KEY="xxxxxxxxxxxxx"
export LLM_PROVIDER="together"
```

**3. Run:**
```bash
./start-web.sh
```

### Cost

| Usage | Cost/Month |
|-------|------------|
| 100 docs | $0.06 |
| 1,000 docs | $0.60 |
| 10,000 docs | $6.00 |

---

## Option 3: Ollama (Self-Hosted)

**Best for:** Development, privacy-sensitive industries, no recurring costs

### Why Ollama?
- ✅ No API costs
- ✅ Full data privacy (runs locally)
- ✅ No internet required
- ✅ Free and open source
- ⚠️ Slow without GPU (600 seconds)
- ⚠️ Fast with GPU (20 seconds, but $0.526/hour)

### Setup

Already documented in `INSTALL.md` - this is the current default.

**Cost:**
- Self-hosted GPU: ~$380/month (g4dn.xlarge 24/7)
- Or spot instances: ~$150/month
- Or use only when needed

**Best Use Case:**
- Healthcare/legal with data privacy requirements
- Enterprise self-hosted deployments
- Development and testing

---

## Option 4: AWS Bedrock

**Best for:** Enterprise customers already on AWS

### Why Bedrock?
- ✅ Enterprise features (CloudWatch, IAM, etc.)
- ✅ Managed service (no ops)
- ✅ Multiple models available
- ⚠️ More expensive than Groq/Together
- ⚠️ Requires AWS account setup

### Setup

**1. Enable Bedrock:**
```bash
# AWS Console → Bedrock → Model access
# Enable: Llama 3.1 8B Instruct
```

**2. Configure AWS credentials:**
```bash
aws configure
# Or use IAM role if on EC2
```

**3. Configure app:**
```bash
export LLM_PROVIDER="bedrock"
export AWS_DEFAULT_REGION="us-east-1"
```

**4. Run:**
```bash
./start-web.sh
```

### Cost

| Usage | Cost/Month |
|-------|------------|
| 100 docs | $0.15 |
| 1,000 docs | $1.50 |
| 10,000 docs | $15.00 |

---

## Option 5: Claude API (Highest Quality)

**Best for:** When you need the absolute best output quality

### Why Claude?
- ✅ Best quality outputs
- ✅ Great for complex documents
- ✅ Fast (5-10 seconds)
- ⚠️ Expensive: $0.03 per document

### Cost

| Usage | Cost/Month |
|-------|------------|
| 100 docs | $3.00 |
| 1,000 docs | $30.00 |
| 10,000 docs | $300.00 |

**Setup:** Coming soon (requires anthropic package)

---

## Recommendation by Use Case

### For Mike (3RVA Quote Generator):
**Use: Groq**
- Setup time: 5 minutes
- Generation time: 5-10 seconds
- Cost: ~$0.04/month for 100 quotes
- Charge: $99/month
- **Best ROI**

### For Healthcare/Legal (Privacy Required):
**Use: Ollama (Self-Hosted)**
- Full data control
- HIPAA/confidentiality compliance
- Higher cost but necessary

### For Enterprise (Already on AWS):
**Use: AWS Bedrock**
- Integrates with existing AWS infrastructure
- CloudWatch monitoring
- IAM access control

### For Highest Quality:
**Use: Claude API**
- Best for complex legal documents
- Superior reasoning
- Worth the cost for high-value documents

---

## Setup Instructions

### 1. Install dependencies (if using API providers)

```bash
# Already included in base installation
pip install httpx  # For API calls
```

### 2. Choose provider and set environment variable

**For Groq:**
```bash
export LLM_PROVIDER="groq"
export GROQ_API_KEY="gsk_xxxxxxxxxxxxx"
```

**For Together:**
```bash
export LLM_PROVIDER="together"
export TOGETHER_API_KEY="xxxxxxxxxxxxx"
```

**For Bedrock:**
```bash
export LLM_PROVIDER="bedrock"
# AWS credentials via aws configure or IAM role
```

**For Ollama (default):**
```bash
# No env vars needed, uses local Ollama
# Or explicitly set:
export LLM_PROVIDER="ollama"
```

### 3. Start the application

```bash
./start-web.sh
```

The app will automatically use the configured provider!

### 4. Verify provider

```bash
# Check health endpoint
curl http://localhost:8000/health

# Should show current provider
{
  "status": "healthy",
  "llm_provider": "groq",
  ...
}
```

---

## Provider Switching

You can switch providers anytime:

```bash
# Start with Groq
export LLM_PROVIDER="groq"
export GROQ_API_KEY="gsk_xxx"
./start-web.sh

# Later switch to Together
pkill -f uvicorn
export LLM_PROVIDER="together"
export TOGETHER_API_KEY="xxx"
./start-web.sh
```

Or use `.env` file:

```bash
# Create .env file
cat > .env <<EOF
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
EOF

# Load automatically
source .env
./start-web.sh
```

---

## Cost Comparison: Self-Hosted vs API

**Self-Hosted GPU (g4dn.xlarge):**
- Cost: $0.526/hour = $380/month (24/7)
- Generation: 20 seconds per document
- Capacity: ~180 docs/hour = 129,600 docs/month
- Cost per doc: $0.003

**Groq API:**
- Cost: $0.0004 per document
- Generation: 5-10 seconds per document
- No infrastructure management
- **7.5x cheaper than self-hosted!**

**Break-even:**
- Self-hosted only cheaper if generating >125,000 docs/month
- For Mike's use case (<1,000/month): **API is 90% cheaper**

---

## Production Deployment Recommendation

### For Small Businesses (Like Mike):

**Use Groq API with simple Windows installer:**

1. **Mike downloads:** `ZettaBrainSkillsSetup.exe`
2. **Installer includes:**
   - Electron desktop app (no Ollama, no Python)
   - Built-in Groq API key (your key)
   - Simple GUI

3. **You charge:** $99/month per business
4. **Your cost:** $0.04 per 100 documents
5. **Your profit:** ~$99/month per customer

**No infrastructure to manage, no GPU costs, huge margins.**

### For Enterprise:

**Hybrid approach:**
- Cloud API by default (Groq/Together)
- Self-hosted option for compliance needs
- Charge $5,000-10,000/year for self-hosted license

---

## Next Steps

1. **Get Groq API key:** https://console.groq.com
2. **Configure:**
   ```bash
   export GROQ_API_KEY="gsk_xxx"
   export LLM_PROVIDER="groq"
   ```
3. **Test:**
   ```bash
   ./start-web.sh
   ```
4. **Generate a document** - see 5-10 second speed!

5. **Build Windows installer** with embedded API key

6. **Deploy to customers** with simple setup

---

## Troubleshooting

### Provider not working

```bash
# Check which provider is active
python3 -c "from zettabrain_skills.llm.factory import get_provider_info; print(get_provider_info())"

# Test provider directly
python3 -c "
from zettabrain_skills.llm.factory import create_llm_provider
provider = create_llm_provider('groq')
print(provider.check_health())
"
```

### Groq rate limit

- Free tier: 30 requests/min
- Solution: Upgrade to paid plan ($0.05-0.10 per 1M tokens)
- Or use Together AI as backup

### AWS Bedrock access denied

```bash
# Check IAM permissions
aws bedrock list-foundation-models

# Ensure model access enabled in console
# AWS Console → Bedrock → Model access
```

---

## Summary

**Recommended for Production:**
1. **Groq** (fast, cheap, simple) ⭐
2. **Together AI** (alternative to Groq)
3. **AWS Bedrock** (enterprise on AWS)

**For Development:**
- **Ollama** (local, private, no costs)

**Your Business Model:**
- Use Groq API: $0.0004 per document
- Charge: $99/month per customer
- Profit: ~$99/month per customer
- **99%+ profit margin**

Get started: `export GROQ_API_KEY="..." && ./start-web.sh` 🚀
