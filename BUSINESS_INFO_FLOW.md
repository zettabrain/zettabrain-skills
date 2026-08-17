# Business Information Data Flow

## Source Location

### **Local Repository:**
```
zettabrain-skills/
└── examples/
    └── discovery-documents/
        ├── 3rva-discovery.md           ← 3RVA business data (loaded automatically)
        └── sample-restaurant-discovery.md  ← Example for other industries
```

### **GitHub Repository:**
```
https://github.com/zettabrain/zettabrain-skills/tree/main/examples/discovery-documents
```

## Data Flow

```
┌─────────────────────────────────────────┐
│  examples/discovery-documents/          │
│  3rva-discovery.md                      │
│                                         │
│  Raw markdown with:                     │
│  - Company info                         │
│  - Products (R-410A, R-22, etc.)        │
│  - Pricing ($85/lb, $150/lb, etc.)      │
│  - Services                             │
│  - Payment terms                        │
└─────────────────┬───────────────────────┘
                  │
                  │ On Web App Startup
                  ▼
┌─────────────────────────────────────────┐
│  zettabrain_skills/web/app.py           │
│  Lines 44-50                            │
│                                         │
│  discovery_path = Path(                 │
│    "examples/discovery-documents/       │
│     3rva-discovery.md"                  │
│  )                                      │
│                                         │
│  parser = DiscoveryParser()             │
│  BUSINESS_INFO = parser.parse_document()│
└─────────────────┬───────────────────────┘
                  │
                  │ LLM Extraction
                  ▼
┌─────────────────────────────────────────┐
│  DiscoveryParser                        │
│  (zettabrain_skills/discovery/parser.py)│
│                                         │
│  Uses Ollama LLM to extract:           │
│  - Structured company data              │
│  - Parsed pricing rules                 │
│  - Service catalog                      │
│  - Policies                             │
└─────────────────┬───────────────────────┘
                  │
                  │ Structured Data
                  ▼
┌─────────────────────────────────────────┐
│  BusinessInfo Object                    │
│  (zettabrain_skills/discovery/models.py)│
│                                         │
│  {                                      │
│    "company_name": "3RVA",              │
│    "industry": "HVAC / Refrigerant",    │
│    "services": [                        │
│      {                                  │
│        "name": "R-410A Refrigerant",    │
│        "pricing": {                     │
│          "unit_price": 85.0,            │
│          "unit": "lb"                   │
│        }                                │
│      },                                 │
│      ...                                │
│    ],                                   │
│    "pricing_rules": [...],              │
│    "payment_terms": "...",              │
│    ...                                  │
│  }                                      │
└─────────────────┬───────────────────────┘
                  │
                  │ Stored in Memory
                  ▼
┌─────────────────────────────────────────┐
│  Global Variables (app.py)              │
│                                         │
│  BUSINESS_INFO = BusinessInfo object    │
│  BUSINESS_CONTEXT = formatted string    │
└─────────────────┬───────────────────────┘
                  │
                  ├─────────────────────┐
                  │                     │
                  ▼                     ▼
┌─────────────────────────┐   ┌──────────────────────┐
│  /discovery Page        │   │  Quote Generation    │
│  Shows business info    │   │  Auto-injects context│
│  - Company details      │   │  into LLM prompt     │
│  - 6 products           │   │  for accurate pricing│
│  - 10+ pricing rules    │   │                      │
│  - Policies             │   │                      │
└─────────────────────────┘   └──────────────────────┘
```

## Example Data in 3rva-discovery.md

### Products Section:
```markdown
1. **R-410A Refrigerant**
   - Most common residential AC refrigerant
   - Available in 25 lb cylinders
   - Price: $85/lb
   - Use: Residential and light commercial AC systems

2. **R-22 Refrigerant (Freon)**
   - Legacy refrigerant for older systems
   - Price: $150/lb
   ...
```

### After LLM Extraction:
```python
BusinessInfo(
    company_name="3RVA",
    industry="HVAC / Refrigerant Supply",
    services=[
        ServiceItem(
            name="R-410A Refrigerant",
            description="Most common residential AC refrigerant",
            pricing=PricingRule(
                item_name="R-410A",
                unit_price=85.0,
                unit="lb"
            )
        ),
        ServiceItem(
            name="R-22 Refrigerant (Freon)",
            description="Legacy refrigerant for older systems",
            pricing=PricingRule(
                item_name="R-22",
                unit_price=150.0,
                unit="lb"
            )
        ),
        ...
    ],
    pricing_rules=[...],
    payment_terms="Net 30 for established accounts...",
    ...
)
```

## Where You Can View It

### 1. **Raw Source File**
**Local:**
```bash
cat examples/discovery-documents/3rva-discovery.md
```

**GitHub:**
https://github.com/zettabrain/zettabrain-skills/blob/main/examples/discovery-documents/3rva-discovery.md

### 2. **Web UI (/discovery page)**
**After starting web app:**
- Go to: `http://localhost:8000/discovery`
- Shows structured data extracted from the markdown file
- Displays:
  - Company details
  - 6 products with pricing
  - 10+ pricing rules
  - Payment terms, warranty, service area

### 3. **CLI Command**
```bash
# Parse and view
zbs discovery parse examples/discovery-documents/3rva-discovery.md

# View previously extracted
zbs discovery info examples/discovery-documents/3rva-discovery-info.json
```

### 4. **In Quote Generation**
When generating a 3RVA quote, this data is automatically injected:
- Customer sees accurate $85/lb for R-410A
- All pricing comes from discovery document
- No hallucinated prices

## How to Update Business Information

### Option 1: Edit the Markdown File
```bash
# Edit the source
nano examples/discovery-documents/3rva-discovery.md

# Restart web app to reload
./start-web.sh
```

### Option 2: Create New Discovery Document
```bash
# Copy template
cp examples/discovery-documents/3rva-discovery.md \
   examples/discovery-documents/my-business.md

# Edit with your business info
nano examples/discovery-documents/my-business.md

# Update app.py to load your file
nano zettabrain_skills/web/app.py
# Change line 44: discovery_path = Path("examples/discovery-documents/my-business.md")
```

### Option 3: CLI Parsing
```bash
# Parse any discovery document
zbs discovery parse my-business-info.md -o my-business-info.json

# Load in Python
from zettabrain_skills.discovery.parser import DiscoveryParser
parser = DiscoveryParser()
business_info = parser.load_business_info(Path("my-business-info.json"))
```

## Key Files

| File | Purpose | Location |
|------|---------|----------|
| **3rva-discovery.md** | Source data (human-readable) | `examples/discovery-documents/` |
| **app.py** | Loads discovery on startup | `zettabrain_skills/web/app.py:44-50` |
| **parser.py** | LLM-based extraction logic | `zettabrain_skills/discovery/parser.py` |
| **models.py** | Data structures | `zettabrain_skills/discovery/models.py` |
| **discovery.html** | Web UI for viewing | `zettabrain_skills/web/templates/discovery.html` |

## Verification

### Check if Data is Loaded
```bash
# Start web app
./start-web.sh

# You should see:
# ✓ Loaded business context for 3RVA

# Check health endpoint
curl http://localhost:8000/health
# Returns: "business_context_loaded": true
```

### View in Browser
1. Go to `http://localhost:8000/discovery`
2. See all 3RVA business information
3. Products listed: R-410A ($85/lb), R-22 ($150/lb), etc.

## Sample Data Summary

**From 3rva-discovery.md:**
- **Company:** 3RVA
- **Industry:** HVAC / Refrigerant Supply
- **Products:** 6 refrigerants + 2 recovery services + 2 consultation services
- **Pricing:** R-410A ($85/lb), R-22 ($150/lb), R-134a ($45/lb), R-404A ($95/lb), R-407C ($70/lb)
- **Pricing Rules:** Bulk discounts, delivery fees, cylinder deposits
- **Payment Terms:** Net 30, credit card, COD
- **Service Area:** Virginia, same-day in Richmond metro

This data ensures every generated quote has accurate, consistent information!
