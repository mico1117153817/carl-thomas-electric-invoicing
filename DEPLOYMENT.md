# Carl Thomas Electric - Invoicing Portal
# ============================================================

## Project Structure
```
carl-thomas-electric/
├── app.py              # FastAPI backend (main application)
├── models.py           # Database models (SQLAlchemy)
├── schemas.py          # Pydantic validation schemas
├── database.py         # Database configuration
├── requirements.txt    # Python dependencies
└── frontend/
    └── index.html      # React-based web interface
```

## Quick Start Guide

### Step 1: Install Dependencies
```bash
cd ~/Desktop/carl-thomas-electric
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
# OR use uvicorn for better performance
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Access the System
- **API Documentation:** http://localhost:8000/docs
- **Web Interface:** http://localhost:8000/frontend/index.html
- **Custom Static Assets:** Configure in app.py static files middleware

## Features Implemented

✅ Customer Management (CRUD)
✅ Invoice Creation with Line Items
✅ Estimate Creation  
✅ Convert Estimates to Invoices
✅ Email Sending (ready for SMTP configuration)
✅ PDF Generation (prepared, pending WeasyPrint integration)
✅ Dashboard with Statistics
✅ Company Branding (Carl Thomas Electric)

## Next Steps / To Complete

1. **PDF Generation:** Add reportlab or weasyprint implementation
2. **Email Configuration:** Set up SMTP credentials in app.py (use environment variables)
3. **Frontend Polish:** Complete the React frontend build system
4. **Testing:** Write unit tests for invoice calculations
5. **Deployment:** Configure for production AWS/Azure hosting

## API Endpoints Available

### Customers
- `POST /api/customers/` - Create customer
- `GET /api/customers/` - List all customers
- `GET /api/customers/{id}` - Get customer details
- `DELETE /api/customers/{id}` - Delete customer

### Invoices  
- `POST /api/invoices/` - Create invoice
- `GET /api/invoices/` - List all invoices
- `GET /api/invoices/{id}` - Get invoice details
- `PUT /api/invoices/{id}/` - Update invoice
- `POST /api/invoices/{id}/send-email/` - Send via email

### Estimates
- `POST /api/estimates/` - Create estimate
- `GET /api/estimates/` - List all estimates  
- `PUT /api/estimates/{id}/` - Update estimate
- `POST /api/estimates/{id}/convert-to-invoice/` - Convert to invoice

## Company Information

**Carl Thomas Electric**
- Email: info@carlthomaselectric.com
- Phone: (555) 123-4567
- Address: [Add your business address here]

---
*Built with FastAPI + React for Carl Thomas Electric*