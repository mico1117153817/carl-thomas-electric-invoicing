"""
SQLAlchemy models for Carl Thomas Electric Invoicing Portal
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlmodel import SQLModel


# Customer model
class Customer(SQLModel, table=True):
    __tablename__ = "customers"
    
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(description="Customer company or individual name", max_length=200)
    email: str = Field(description="Customer contact email", max_length=255)
    phone: str = Field(default=None, description="Contact phone number")
    address: str = Field(default=None, description="Billing/shipping address")
    notes: str = Field(default=None, description="Additional notes about customer")


# Invoice model
class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"
    
    id: int | None = Field(default=None, primary_key=True)
    invoice_number: str = Field(description="Unique invoice number like INV-001")
    customer_id: int = Field(
        description="Customer ID",
        foreign_key="customers.id"
    )
    date_issued: datetime = Field(
        default_factory=datetime.now,
        description="Date invoice was issued"
    )
    due_date: datetime = Field(
        description="Payment due date (default 30 days from issue)",
        sa_column=Column(DateTime)
    )
    status: str = Field(
        default="pending",
        description="Invoice status: pending, paid, overdue, sent"
    )
    notes: str = Field(default=None, description="Notes about this invoice")
    subtotal: float = Field(default=0.0, description="Subtotal before taxes")
    tax_amount: float = Field(default=0.0, description="Tax amount")
    total_amount: float = Field(default=0.0, description="Invoice total amount")
    estimated_source_id: int | None = Field(
        default=None,
        description="Original estimate ID this invoice came from"
    )


# Estimate model
class Estimate(SQLModel, table=True):
    __tablename__ = "estimates"
    
    id: int | None = Field(default=None, primary_key=True)
    estimate_number: str = Field(description="Unique estimate number like EST-001")
    customer_id: int = Field(
        description="Customer ID",
        foreign_key="customers.id"
    )
    date_created: datetime = Field(
        default_factory=datetime.now,
        description="Date estimate was created"
    )
    expiration_date: datetime | None = Field(
        default=None,
        description="Estimate expiration date"
    )
    status: str = Field(
        default="draft",
        description="Estimate status: draft, active, completed, voided"
    )
    notes: str = Field(default=None, description="Notes about this estimate")


class InvoiceItem(SQLModel, table=True):
    """Invoice line items"""
    __tablename__ = "invoice_items"
    
    id: int | None = Field(default=None, primary_key=True)
    invoice_id: int = Field(
        foreign_key="invoices.id",
        index=True
    )
    description: str = Field(description="Item description")
    quantity: float = Field(default=1.0, description="Quantity of item")
    unit_price: float = Field(default=0.0, description="Price per unit")
    tax_rate: float = Field(
        default=0.0,
        description="Tax rate as percentage (divide by 100)"
    )


class EstimateItem(SQLModel, table=True):
    """Estimate line items"""
    __tablename__ = "estimate_items"
    
    id: int | None = Field(default=None, primary_key=True)
    estimate_id: int = Field(
        foreign_key="estimates.id",
        index=True
    )
    description: str = Field(description="Item description")
    quantity: float = Field(default=1.0, description="Quantity of item")
    unit_price: float = Field(default=0.0, description="Price per unit")

