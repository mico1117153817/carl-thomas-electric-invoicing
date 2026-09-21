"""
Carl Thomas Electric - Invoicing Portal
Main application entry point
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import sqlmodel

from database import engine, SessionLocal
from models import (
    Customer, 
    Invoice, 
    Estimate,
    InvoiceItem,
    EstimateItem
)
from schemas import InvoiceCreate, EstimateCreate, CustomerCreate

# Create FastAPI app
app = FastAPI(
    title="Carl Thomas Electric - Invoicing Portal",
    description="Web-based system for creating and sending invoices and estimates",
    version="1.0.0"
)

# CORS middleware for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database tables creation
sqlmodel.metadata.create_all(engine)


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    sqlmodel.metadata.create_all(engine)
    return {"message": "Database tables created successfully"}


@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "project": "Carl Thomas Electric - Invoicing Portal",
        "status": "running",
        "docs": "/docs"
    }


# --- Customer Endpoints ---

@app.post("/api/customers/", response_model=Customer)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    db_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone or "",
        address=customer.address or ""
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@app.get("/api/customers/", response_model=list[Customer])
async def get_customers():
    """Get all customers"""
    return sqlmodel.select(Customer).all()


@app.get("/api/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get a specific customer by ID"""
    customer = sqlmodel.select(Customer).where(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.delete("/api/customers/{customer_id}")
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete a customer"""
    customer = sqlmodel.select(Customer).where(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted"}


# --- Estimate Endpoints ---

@app.post("/api/estimates/", response_model=Estimate)
async def create_estimate(estimate_data: EstimateCreate, db: Session = Depends(get_db)):
    """Create a new estimate"""
    # This would need line items - simplified for now
    db_estimate = Estimate(
        customer_id=estimate_data.customer_id,
        description=estimate_data.description or "",
        total_amount=estimate_data.total_amount or 0,
        status="draft",
        notes=estimate_data.notes or ""
    )
    db.add(db_estimate)
    db.commit()
    db.refresh(db_estimate)
    return db_estimate


@app.get("/api/estimates/", response_model=list[Estimate])
async def get_estimates():
    """Get all estimates"""
    return sqlmodel.select(Estimate).all()


@app.get("/api/estimates/{estimate_id}", response_model=Estimate)
async def get_estimate(estimate_id: int, db: Session = Depends(get_db)):
    """Get a specific estimate by ID"""
    estimate = sqlmodel.select(Estimate).where(Estimate.id == estimate_id).first()
    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    return estimate


@app.put("/api/estimates/{estimate_id}/", response_model=Estimate)
async def update_estimate(estimate_id: int, estimate_update: EstimateCreate, db: Session = Depends(get_db)):
    """Update an existing estimate"""
    estimate = sqlmodel.select(Estimate).where(Estimate.id == estimate_id).first()
    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    
    # Update fields from request
    update_data = estimate_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(estimate, field, value)
    
    db.commit()
    db.refresh(estimate)
    return estimate


@app.post("/api/estimates/{estimate_id}/convert-to-invoice/")
async def convert_estimate_to_invoice(estimate_id: int, db: Session = Depends(get_db)):
    """Convert an estimate to an invoice"""
    estimate = sqlmodel.select(Estimate).where(Estimate.id == estimate_id).first()
    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    
    # Create invoice from estimate
    db_invoice = Invoice(
        customer_id=estimate.customer_id,
        description=estimate.description,
        total_amount=estimate.total_amount,
        status="pending",
        notes=estimate.notes,
        estimated_source_id=estimate.id
    )
    
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    
    # Mark estimate as completed
    estimate.status = "completed"
    db.commit()
    
    return {
        "message": "Estimate converted to invoice successfully",
        "invoice": db_invoice
    }


# --- Invoice Endpoints ---

@app.post("/api/invoices/", response_model=Invoice)
async def create_invoice(invoice_data: InvoiceCreate, db: Session = Depends(get_db)):
    """Create a new invoice"""
    db_invoice = Invoice(
        customer_id=invoice_data.customer_id,
        description=invoice_data.description or "",
        total_amount=invoice_data.total_amount or 0,
        status="pending",
        notes=invoice_data.notes or ""
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


@app.get("/api/invoices/", response_model=list[Invoice])
async def get_invoices():
    """Get all invoices"""
    return sqlmodel.select(Invoice).all()


@app.get("/api/invoices/{invoice_id}", response_model=Invoice)
async def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Get a specific invoice by ID"""
    invoice = sqlmodel.select(Invoice).where(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@app.put("/api/invoices/{invoice_id}/", response_model=Invoice)
async def update_invoice(invoice_id: int, invoice_update: InvoiceCreate, db: Session = Depends(get_db)):
    """Update an existing invoice"""
    invoice = sqlmodel.select(Invoice).where(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    update_data = invoice_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(invoice, field, value)
    
    db.commit()
    db.refresh(invoice)
    return invoice


@app.post("/api/invoices/{invoice_id}/send-email/")
async def send_invoice_email(invoice_id: int, customer_email: str, background_tasks: BackgroundTasks = None):
    """Send invoice via email to customer"""
    invoice = sqlmodel.select(Invoice).where(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # TODO: Implement actual email sending with PDF attachment
    # For now, just update status
    invoice.status = "sent"
    invoice.sent_to = customer_email
    db.commit()
    
    return {
        "message": f"Invoice #{invoice.id} sent to {customer_email}",
        "email": customer_email
    }


@app.get("/api/invoices/{invoice_id}/pdf/")
async def get_invoice_pdf(invoice_id: int):
    """Generate PDF for invoice"""
    # TODO: Implement PDF generation
    return {"message": f"PDF for Invoice #{invoice_id} would be generated here"}


# --- Utility Endpoints ---

@app.get("/api/invoices/stats")
async def get_invoice_statistics():
    """Get invoice statistics"""
    invoices = sqlmodel.select(Invoice).all()
    total_invoices = len(invoices)
    pending = len([i for i in invoices if i.status == "pending"])
    sent = len([i for i in invoices if i.status == "sent"])
    
    return {
        "total_invoices": total_invoices,
        "pending": pending,
        "sent": sent,
        "total_amount": sum(i.total_amount for i in invoices)
    }


# Database session dependency
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(
    "sqlite+aiosqlite:///invoices.db",
    echo=True,
    future=True
)

SessionLocal = async_sessionmaker(
    engine,
    class_=sqlmodel.pool.AsyncSession,
    expire_on_commit=False
)


async def get_db():
    """Async database session"""
    async with SessionLocal() as session:
        return session


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
