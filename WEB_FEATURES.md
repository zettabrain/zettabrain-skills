# ZettaBrain Skills Web Application Features

Complete web interface for multi-industry document generation with discovery document support.

## 🎯 Key Features

### 1. Multi-Industry Skill Selection

**Home Page** (`/`)
- Visual skill selector with industry cards
- Choose from 7+ industry-specific templates:
  - **3RVA Quote Generator** - HVAC refrigerant quotes
  - **Legal Contract Review** - Contract analysis and risk assessment
  - **Medical Patient Intake** - Healthcare intake forms
  - **Real Estate Listing** - Property descriptions
  - **Restaurant Menu Description** - Appetizing menu items
  - **Sales Proposal** - B2B proposals
  - More skills auto-discovered from `examples/` directory

**How it works:**
1. Click on any industry skill card
2. Skill information appears below
3. Enter your request details
4. Add customer information (optional)
5. Generate document

### 2. Discovery Document Management

**Business Info Page** (`/discovery`)
- View loaded business information
- Company details (name, industry, contact info)
- Products & services with pricing
- Pricing rules and markups
- Payment terms, warranties, service area
- Visual cards and organized sections

**Auto-Loading:**
- Web app automatically loads `examples/discovery-documents/3rva-discovery.md` on startup
- Business context injected into all relevant document generation requests
- Ensures accurate pricing and consistent information

### 3. Universal Document Management

**Generated Documents Page** (`/generated`)
- List all generated documents across all industries
- Document cards with:
  - Customer name and request preview
  - Skill type badge
  - Generation date and time
  - Customer email/phone if provided
  - Document content preview
- Quick actions:
  - View full document
  - Download as PDF

**Document Viewer** (`/document/{id}`)
- Full document display with metadata
- Success banner
- Organized customer information
- Document content in monospace format
- Action buttons:
  - Download PDF
  - Copy to clipboard
  - Generate another document
  - View all documents

### 4. PDF Export

**PDF Generation** (`/document/{id}/pdf`)
- Professional PDF formatting
- ZettaBrain branding
- Document metadata header
- Clean typography
- Suitable for client delivery

## 🎨 User Interface

### Design
- Clean white background (Onyx-inspired)
- ZettaBrain logo in navbar
- Consistent color scheme (#5b64f4 primary blue)
- Mobile-responsive layouts
- Professional typography

### Navigation
- **Home** - Generate new documents
- **Generated Documents** - View history
- **Business Info** - View loaded discovery data

### Components
- Skill cards with hover effects
- Success banners
- Metadata grids
- Preview cards
- Action buttons
- Empty states

## 📱 Mobile Support

- Fully responsive design
- Touch-friendly buttons
- Optimized layouts for phone/tablet
- Accessible from any device
- Perfect for field use

## 🔄 Backwards Compatibility

### Legacy 3RVA Routes
- `/3rva` - Original 3RVA-specific interface
- `/quotes` - Redirects to `/generated`
- `/quote/{id}` - Redirects to `/document/{id}`
- `/quote/{id}/pdf` - Redirects to `/document/{id}/pdf`

All existing 3RVA functionality preserved.

## 🚀 Usage Examples

### Example 1: Generate 3RVA Quote
1. Go to `/` home page
2. Click "3RVA Quote Full" card
3. Enter customer request: "Need 100 lbs R-410A for same-day delivery"
4. Add customer details
5. Click "Generate Document"
6. View quote, download PDF

### Example 2: Generate Legal Contract Review
1. Go to `/` home page
2. Click "Legal Contract Review" card
3. Paste contract text
4. Click "Generate Document"
5. Receive risk assessment with action items

### Example 3: View Business Information
1. Go to `/discovery`
2. See loaded 3RVA business data:
   - 6+ products with pricing
   - 10+ pricing rules
   - Payment terms
   - Service area
3. Use for reference when generating quotes

### Example 4: Browse Generated Documents
1. Go to `/generated`
2. See all past documents
3. Click any card to view full document
4. Download PDFs as needed

## 🎯 Demo Flow for Mike (3RVA)

1. **Show Platform Capability**
   - Open `/` home page
   - Point out multiple industries supported
   - "This isn't built just for 3RVA - it's a platform"

2. **Show Business Context**
   - Navigate to `/discovery`
   - Show loaded 3RVA information
   - "All your pricing and products are automatically included"

3. **Generate Sample Quote**
   - Return to home, select 3RVA skill
   - Enter sample customer request
   - Generate quote in 30-60 seconds
   - Show current date, accurate pricing

4. **Show PDF Export**
   - Download PDF
   - Professional formatting with ZettaBrain branding
   - Ready to send to customer

5. **Show Document Library**
   - Go to `/generated`
   - Show past quotes
   - Easy retrieval and reference

6. **Show Other Industries**
   - "We can do the same for other businesses"
   - "Legal firms, medical practices, real estate agents"
   - "Same platform, different skills"

## 🛠️ Technical Features

### Auto-Discovery
- Skills automatically loaded from `examples/` directory
- No hard-coded skill list
- Add new skills by dropping `.md` files in `examples/`

### State Management
- In-memory document storage (50 most recent)
- Business context loaded once at startup
- Fast response times

### Performance
- 30-60 seconds generation time on GPU instance
- Async document generation
- No blocking operations

### Error Handling
- Ollama health checks
- Graceful error messages
- User-friendly suggestions

## 📊 Health Check

**Endpoint:** `/health`

Returns:
```json
{
  "status": "healthy",
  "ollama": "running",
  "business_context_loaded": true,
  "business_name": "3RVA",
  "version": "0.5.0"
}
```

## 🔧 Setup

1. Start web server:
   ```bash
   ./start-web.sh
   ```

2. Access from:
   - **Local:** http://localhost:8000
   - **Phone/Tablet:** http://<ec2-public-ip>:8000

3. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

## 📝 Adding New Skills

1. Create skill file in `examples/`:
   ```markdown
   ---
   name: my-new-skill
   version: 1.0.0
   description: What this skill does
   business_type: industry-name
   ---
   
   # Skill Instructions
   ...
   ```

2. Restart web application
3. New skill appears automatically on home page

## 🎁 Value Proposition

### For 3RVA (Mike)
- **Fast:** Generate quotes in under a minute
- **Accurate:** Loaded pricing ensures correctness
- **Professional:** Branded PDFs ready for customers
- **Mobile:** Use from phone in the field
- **Consistent:** Same information every time

### For Platform Demo
- **Multi-Industry:** Works for any business sector
- **Scalable:** Add new skills easily
- **White-Label Ready:** Rebrand for any client
- **Self-Hosted:** No API costs, full data control
- **Open Source:** Transparent, customizable

## 🔮 Next Steps

- [ ] Add discovery document upload interface
- [ ] Implement document search/filter
- [ ] Add batch document generation
- [ ] Create document templates library
- [ ] Add user authentication
- [ ] Implement document versioning
- [ ] Add analytics dashboard

## 📞 Support

For issues or questions about the web application:
- Check `/health` endpoint for system status
- Review browser console for errors
- Ensure Ollama is running and accessible
- Verify discovery document exists if using business context
