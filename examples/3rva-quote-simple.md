---
name: 3rva-quote-simple
version: 1.0.0
description: Generate service quotes for 3RVA refrigerant services (sales, recovery, buyback). Use when customer requests pricing for refrigerant, mentions needing a quote, or asks "how much for" refrigerant services.
business_type: service
author: ZettaBrain
temperature: 0.2
max_tokens: 1500
requires_discovery:
  - pricing-rules
tags:
  - quote
  - pricing
  - 3rva
  - refrigerant
  - customer-facing
---

# 3RVA Service Quote Generator

Generate professional quotes for 3RVA refrigerant services.

## Purpose

Turn customer quote requests into complete, structured quotes while identifying any missing information needed for accurate pricing.

## Procedure

1. **Parse the customer request**
   - Identify service type (sale, recovery, or buyback)
   - Extract refrigerant type (R-22, R-410A, R-134a, etc.)
   - Note quantity, location, and timeline
   - Identify if customer is new or existing

2. **Check for missing information**
   - Compare against required fields for that service type
   - List ALL missing details before proceeding
   - Distinguish between required vs. nice-to-have

3. **Draft the quote**
   - Use standard format below
   - Be specific about what's included
   - State assumptions explicitly if any
   - Flag if needs manager approval

## Required Information by Service Type

### Refrigerant Sale
- Refrigerant type and quantity (lbs)
- Delivery location (city/ZIP)
- Delivery date needed
- New vs. reclaimed
- Cylinder size preference
- Whether cylinders will be returned

### Recovery Job
- Site type and location
- Refrigerant type
- Estimated system charge
- Pressure class (high/medium/low)
- Access requirements (normal/secure site)
- Timeline (regular/rush)

### Buyback
- Refrigerant type
- Estimated quantity
- Current condition
- Whether 3RVA recovered it
- Cylinder information

## Output Format

```
QUOTE - [Service Type]
Prepared for: [Customer Name if known, or "Customer"]
Date: [Today's date]
Reference: [Quote number if available, or "DRAFT"]

SCOPE
[Clear description of what will be provided/performed]

PRICING
NOTE: This is a preliminary quote structure. Actual pricing requires 
discovery data (pricing-rules.md) to be populated.

[Service] - [Quantity/Unit]
[Additional services if applicable]

IMPORTANT - MISSING INFORMATION:
- [List each missing required field]
- [Each on its own line]

NEXT STEPS
1. Gather missing information from customer
2. Finalize pricing using 3RVA pricing rules
3. Review and send final quote

ASSUMPTIONS (if any):
- [List any assumptions made]
```

## Escalation Flags

Flag for manager review if:
- Total value appears to exceed $50,000
- Customer is new and order is substantial
- Non-standard terms requested
- Unusual refrigerant type or configuration
- Security clearance or special access required

## Example

**Input**: "Need 100 lbs of R-22 for a job in Richmond, VA by Friday"

**Output**: 
- Identify: Refrigerant sale, 100 lbs R-22, Richmond VA, deadline Friday
- Missing: New vs reclaimed, cylinder size, return policy, exact delivery address, customer name
- Draft quote with clear MISSING INFORMATION section
- Normal escalation (under threshold)

## Never

- Never invent pricing (note that pricing rules are required)
- Never commit to delivery dates without inventory check
- Never skip listing missing information
- Never make regulatory claims (defer to compliance skill)
- Never assume customer type (ask if new vs. existing)

## Tone

Professional but friendly. 3RVA customers are contractors and facility managers who want clarity and speed. No corporate jargon.
