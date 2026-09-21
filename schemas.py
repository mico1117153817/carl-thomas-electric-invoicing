"""
Pydantic schemas for Carl Thomas Electric Invoicing Portal
"""
from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel


class CustomerBase(SQLModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    notes: str | None = None


class CustomerCreate(CustomerBase):
    """Schema for creating a customer"""
    pass


# Invoicing schemas with line items
from typing import List


class InvoiceItem(SQLModel):
    description: str
    quantity: float | None = 1.0
    unit_price: float | None = None
    
    @property
    def total(self) -> float:
        if self.quantity and self.unit_price:
            return self.quantity * self.unit_price
        return 0.0


class InvoiceCreate(BaseModel):
    customer_id: int
    description: str | None = None
    notes: str | None = None
    total_amount: float | None = None
    
    # Add line items support
    items: Optional[typing.List[InvoiceItem]] = None


class InvoiceUpdate(InvoiceCreate):
    """Schema for updating invoice"""
    pass