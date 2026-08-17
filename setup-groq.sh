#!/bin/bash
# Quick setup script for Groq provider
# Makes ZettaBrain Skills run fast without GPU

echo "========================================="
echo "  ZettaBrain Skills - Groq Setup"
echo "========================================="
echo ""

# Check if Groq API key is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "❌ GROQ_API_KEY not set"
    echo ""
    echo "Get your free API key at: https://console.groq.com"
    echo ""
    echo "Then set it:"
    echo "  export GROQ_API_KEY=\"gsk_xxxxxxxxxxxxx\""
    echo ""
    echo "Or add to ~/.bashrc:"
    echo "  echo 'export GROQ_API_KEY=\"gsk_xxx\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    echo ""
    exit 1
fi

echo "✓ GROQ_API_KEY found"

# Set provider
export LLM_PROVIDER="groq"
echo "✓ LLM_PROVIDER set to groq"

# Test connection
echo ""
echo "Testing Groq connection..."
python3 -c "
from zettabrain_skills.llm.providers.groq_provider import GroqProvider
try:
    provider = GroqProvider()
    if provider.check_health():
        print('✓ Groq API connection successful!')
        print('  Model:', provider.model)
        print('  Provider:', provider.get_model_info()['provider'])
    else:
        print('❌ Groq API connection failed')
        exit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    exit(1)
" || exit 1

echo ""
echo "========================================="
echo "  Setup Complete! 🎉"
echo "========================================="
echo ""
echo "Start the web application:"
echo "  ./start-web.sh"
echo ""
echo "Or test with CLI:"
echo "  zbs generate examples/3rva-quote-full.md \\"
echo "    --input \"Need 100 lbs R-410A\""
echo ""
echo "Generation time: 5-10 seconds (vs 600s on CPU!)"
echo "Cost: ~\$0.0004 per document"
echo ""
