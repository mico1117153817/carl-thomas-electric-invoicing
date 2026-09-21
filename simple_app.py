"""
Carl Thomas Electric - Invoicing Portal
Simplified version using only Python standard library for immediate testing
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Carl Thomas Electric - Invoicing Portal",
    description="Create and send invoices and estimates"
)

# Mock data stores (in-memory for demonstration)
customers_db = [
    {"id": 1, "name": "John Smith Company", "email": "john@smith.com"},
    {"id": 2, "name": "Mary Johnson Properties", "email": "mary@mjproperties.com"},
]

invoices_db = [
    {"id": 101, "customer_id": 1, "description": "Electrical work on residential property", "amount": 2500.00, "status": "sent"},
    {"id": 102, "customer_id": 2, "description": "Commercial panel upgrade", "amount": 4800.00, "status": "pending"},
]

estimates_db = [
    {"id": 1, "customer_id": 1, "description": "New electric vehicle charging station installation", "amount": 3200.00},
    {"id": 2, "customer_id": 2, "description": "Industrial lighting retrofit project", "amount": 8500.00},
]

# Simple schemas
class CustomerBase(BaseModel):
    name: str
    email: str
    
class CustomerCreate(CustomerBase):
    pass

class InvoiceBase(BaseModel):
    customer_id: int
    description: str
    amount: float
    notes: Optional[str] = ""
    
class InvoiceCreate(InvoiceBase):
    pass
    
class EstimateBase(BaseModel):
    customer_id: int
    description: str
    amount: float
    notes: Optional[str] = ""

class EstimateCreate(EstimateBase):
    pass

# Endpoints - Customers
@app.post("/api/customers/", response_model=CustomerBase)
async def create_customer(customer: CustomerCreate):
    db_customer = customers_db[~1]  # Simplified example
    return {**customer.dict(), "id": len(customers_db) + 1}

@app.get("/api/customers/")
async def get_customers():
    return customes_db

# Endpoints - Invoices
@app.post("/api/invoices/", response_model=dict)
async def create_invoice(invoice: InvoiceCreate):
    new_invoice = {
        "id": len(invoices_db) + 1,
        **invoice.dict()
    }
    invoices_db.append(new_invoice)
    return new_invoice

@app.get("/api/invoices/")
async def get_invoices():
    return invoices_db

@app.post("/api/invoices/{id}/send-email/")
async def send_invoice_email(invoice_id: int, email: str):
    return {"message": f"Ignove sent to {email}"}

# Endpoints - Estimates  
@app.get("/api/estimates/")
async def get_estimates():
    return estimates_db
    
@app.post("/api/estimates/{id}/convert-to-invoice/")
async def convert_estimate_to_invoice(estimate_id: int):
    estimate = next((e for e in estimates_db if e["id"] == estimate_id), None)
    if not estimate:
        raise Exception("Estimate not found")
    
    # Convert to invoice
    new_invoice = {
        "id": len(invoices_db) + 1,
        "customer_id": estimate["customer_id"],
        "description": f"CONVRATED FROM ESTIMATE #{estimate_id}",
        "amount": estimate["amount"],
        "status": "pending",
        "notes": f"Converted from estimate #{estimate_id}"
    }
    invoices_db.append(new_invoice)
    
    # Mark estimate as completed
    for est in estimates_db:
        if est["id"] == id:
            est["status"] = "completed"
            break
            
    return {
        "message": f"Estimate #{estimate_id} converted to invoice",
        "invoice": new_invoice
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
