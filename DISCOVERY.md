# Discovery Document Processing

ZettaBrain Skills can automatically extract business information from discovery documents to populate skills with accurate pricing, services, and policies.

## Overview

Discovery documents are structured markdown files that describe a business's:
- Products and services
- Pricing rules and structures
- Contact information
- Policies (payment terms, warranties, service area)
- Target customers

The discovery processor uses LLMs to extract this information into structured JSON that can be automatically injected into document generation requests.

## Quick Start

### 1. Create a Discovery Document

See `examples/discovery-documents/` for templates:
- `3rva-discovery.md` - HVAC/refrigerant supply company
- `sample-restaurant-discovery.md` - Restaurant business

### 2. Parse the Discovery Document

```bash
# Parse and extract business information
zbs discovery parse examples/discovery-documents/3rva-discovery.md

# Output saved to: examples/discovery-documents/3rva-discovery-info.json
```

### 3. View Extracted Information

```bash
# Display structured business info
zbs discovery info examples/discovery-documents/3rva-discovery-info.json
```

### 4. Use in Web Application

The web app automatically loads business context from discovery documents. Just ensure your discovery document exists at:
```
examples/discovery-documents/3rva-discovery.md
```

The system will:
1. Parse the discovery document on startup
2. Extract pricing rules, services, and policies
3. Automatically inject this context into all quote generation requests

## Discovery Document Format

```markdown
# Company Name Business Discovery Document

## Company Information

**Company Name:** Your Company
**Industry:** Your Industry
**Description:** What your company does

## Contact Information

**Phone:** (555) 123-4567
**Email:** contact@company.com
**Address:** 123 Main St
**Website:** www.company.com

## Products & Services

### Product Category 1

1. **Product/Service Name**
   - Description of what it is
   - Available in X units
   - Price: $XX per unit
   - Use: What it's used for

### Service Category 1

1. **Service Name**
   - What's included
   - Price: $XX per hour/unit
   - Minimum: X hours/units

## Pricing Rules

- Rule 1: Details
- Rule 2: Details
- Bulk discounts
- Delivery fees

## Payment Terms

- Net 30 for approved accounts
- Credit card accepted
- COD terms

## Warranty & Guarantees

- Your warranty policy
- Return policy
- Guarantees

## Service Area

Geographic area served, delivery options

## Business Hours

Operating hours and emergency service availability
```

## Extracted Data Structure

The parser extracts information into a structured format:

```json
{
  "company_name": "3RVA",
  "industry": "HVAC / Refrigerant Supply",
  "description": "Brief company description",
  "contact_email": "sales@3rva.com",
  "contact_phone": "(804) 555-3RVA",
  "address": "123 Industrial Parkway, Richmond, VA 23230",
  "website": "www.3rva.com",
  "services": [
    {
      "name": "R-410A Refrigerant",
      "description": "Most common residential AC refrigerant",
      "category": "Refrigerants",
      "pricing": {
        "item_name": "R-410A",
        "unit_price": 85.0,
        "unit": "lb"
      }
    }
  ],
  "pricing_rules": [
    {
      "item_name": "R-410A",
      "unit_price": 85.0,
      "unit": "lb",
      "notes": "25 lb cylinders"
    }
  ],
  "payment_terms": "Net 30 for established accounts",
  "warranty_policy": "30-day satisfaction guarantee",
  "service_area": "Virginia, same-day delivery in Richmond metro"
}
```

## CLI Commands

### Parse Discovery Document

```bash
zbs discovery parse <document-path> [OPTIONS]

Options:
  --output, -o PATH      Output JSON file path (default: <document>-info.json)
  --ollama-url URL       Ollama API URL (default: http://localhost:11434)
  --model MODEL          LLM model to use (default: llama3.1:8b)
  --timeout SECONDS      Request timeout (default: 300)

Examples:
  # Basic parsing
  zbs discovery parse examples/discovery-documents/3rva-discovery.md

  # Custom output location
  zbs discovery parse my-business.md -o my-business-info.json

  # Use different model
  zbs discovery parse my-business.md --model llama3.1:70b
```

### View Extracted Information

```bash
zbs discovery info <info-json-path>

Example:
  zbs discovery info examples/discovery-documents/3rva-discovery-info.json
```

## Integration with Skills

Discovery documents enhance skill generation by:

1. **Automatic Context Injection**: Business information is automatically added to generation requests
2. **Accurate Pricing**: LLM has access to exact pricing rules
3. **Consistent Information**: Contact info, policies, and terms are consistent across all documents
4. **Service Details**: Complete service catalog available for quotes

### Example: Quote Generation with Discovery

Without discovery document:
```bash
zbs generate examples/3rva-quote-full.md \
  --input "Need 100 lbs of R-410A"
```

The LLM must infer or hallucinate pricing and details.

With discovery document (web app):
1. Discovery document parsed on startup
2. Business context automatically included:
   - R-410A costs $85/lb
   - Available in 25 lb cylinders
   - Delivery fees and payment terms
   - Contact information
3. Quote generated with accurate, consistent information

## Benefits

### For Business Owners
- **Consistency**: All documents use the same pricing and policies
- **Easy Updates**: Update discovery document once, all quotes reflect changes
- **No Training**: LLM automatically learns your business without manual prompt engineering

### For Developers
- **Structured Data**: Clean JSON format for integration
- **Flexible Parsing**: LLM-based extraction handles variations in format
- **Extensible**: Easy to add new fields or validation rules

### For End Users (Customers)
- **Accurate Quotes**: Pricing and terms are correct every time
- **Professional**: Consistent formatting and information
- **Complete**: All necessary details included automatically

## Advanced Usage

### Custom Extraction Prompts

Modify `zettabrain_skills/discovery/parser.py` to customize what information is extracted:

```python
EXTRACTION_PROMPT = """
Extract additional fields:
- certifications
- insurance coverage
- employee count
...
"""
```

### Validation Rules

Add validation for extracted data:

```python
def validate_business_info(business_info: BusinessInfo):
    """Validate extracted business information."""
    if not business_info.pricing_rules:
        raise ValueError("No pricing rules extracted")

    if business_info.industry == "healthcare":
        assert business_info.certifications, "Healthcare requires certifications"
```

### Multiple Discovery Documents

Support multiple businesses:

```python
# Load different discovery docs for different business_ids
business_contexts = {
    "3rva": load_discovery("3rva-discovery.md"),
    "restaurant": load_discovery("restaurant-discovery.md"),
    "medical": load_discovery("medical-discovery.md")
}

# Use in generation
context = business_contexts[business_id]
```

## Troubleshooting

### Extraction Quality Issues

If the LLM misses information:
1. Make your discovery document more explicit
2. Use clear section headers
3. Format pricing as: `Price: $XX/unit`
4. Increase model size (llama3.1:70b for better extraction)

### Parsing Errors

If parsing fails:
1. Check discovery document format (must be valid markdown)
2. Ensure Ollama is running: `ollama serve`
3. Increase timeout for large documents: `--timeout 600`
4. Check extraction notes in output JSON

### Performance

Parsing takes 30-60 seconds per document:
- Run once at startup (web app)
- Cache extracted JSON
- Re-parse only when discovery document changes

## Future Enhancements

- [ ] Watch discovery documents for changes and auto-reload
- [ ] Multi-language support
- [ ] Image/table extraction from PDFs
- [ ] Discovery document validation and linting
- [ ] Template generation from extracted data
- [ ] API endpoint for discovery management

## Examples

See `examples/discovery-documents/` for:
- `3rva-discovery.md` - Full HVAC company example
- `sample-restaurant-discovery.md` - Restaurant business example

Create your own discovery documents following these templates for any industry.
