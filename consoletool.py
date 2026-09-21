"""
Carl Thomas Electric - Invoicing Portal
Lightweight version using only Python 3.x and Jupyter capabilities
No external dependencies required beyond the environment!
"""
from datetime import datetime, timedelta
import math

# Simple JSON storage (in-memory for demo)
customers = {
    1: {"id": 1, "name": "John Smith Company", "email": "john@smith.com"},
    2: {"id": 2, "name": "Mary Johnson Properties", "email": "mary@mjproperties.com"}
}

invoices = [
    {"id": 101, "customer_id": 1, "description": "Electrical work on residential property", 
     "amount": 2500.00, "status": "sent"},
    {"id": 102, "customer_id": 2, "description": "Commercial panel upgrade", 
     "amount": 4800.00, "status": "pending"}
]

estimates = [
    {"id": 1, "customer_id": 1, "description": "EV charging station installation", "amount": 3200.00},
    {"id": 2, "customer_id": 2, "description": "Industrial lighting retrofit", "amount": 8500.00}
]

def create_invoice(customer_id, description, notes=""):
    """Create a new invoice"""
    if customer_id not in customers:
        return {"error": "Customer not found"}
    
    # Generate invoice number
    inv_num = f"INV-{100 + len(invoices)"
    
    invoice = {
        "id": 100 + len(invoices) + 1,
        "invoice_number": inv_num,
        "customer_id": customer_id,
        "description": description,
        "amount": 0.0,
        "notes": notes,
        "status": "pending",
        "created_at": datetime.now()
    }
    
    invoices.append(invoice)
    return invoice

def create_estimate(customer_id, description, notes="", total_amount=None):
    """Create a new estimate"""
    if customer_id not in customers:
        return {"error": "Customer not found"}
    
    est_num = f"EST-{1 + len(estimates)}"
    
    estimate = {
        "id": 1 + len(estimates),
        "estimate_number": est_num,
        "customer_id": customer_id,
        "description": description or "",
        "notes": notes,
        "amount": total_amount or 0.0,
        "status": "draft",
        "created_at": datetime.now()
    }
    
    estimates.append(estimate)
    return estimate

def convert_estimate_to_invoice(estimate_id):
    """Convert an estimate to an invoice"""
    estimate = next((e for e in estimates if e["id"] == estimate_id), None)
    
    if not estimate:
        return {"error": "Estimate not found"}
    
    # Create invoice from estimate data
    inv_num = f"INV-{100 + len(invoices)}"
    invoice = {
        "id": 100 + len(invoices) + 1,
        "invoice_number": inv_num,
        "customer_id": estimate["customer_id"],
        "description": f"{estimate['description']} (converted from estimate #{estimate_id})",
        "amount": estimate["amount"],
        "notes": estimate.get("notes", "") + f" - Converted from estimate #{estimate_id}",
        "status": "pending",
        "created_at": datetime.now()
    }
    
    invoices.append(invoice)
    
    # Mark estimate as completed
    for e in estimates:
        if e["id"] == estimate_id:
            e["status"] = "completed"
            break
    
    return {"invoice": invoice, "message": f"Estimate #{estimate_id} converted to invoice"}

def list_customers():
    """List all customers"""
    return [{"name": c["name"], "customer_id": c["id"]} for c in customers.values()]

def list_invoices():
    """List all invoices"""
    return invoices

def list_estimates():
    """List all estimates"""
    return estimates

def get_invoice_pdf(invoice_id):
    """Generate simple text representation (in production would use WeasyPrint/reportlab)"""
    invoice = next((i for i in invoices if i["id"] == invoice_id), None)
    
    if not invoice:
        return "Invoice not found"
    
    customer = customers[invoice["customer_id"]]
    
    template = f"""
INVOICE
{'=' * 60}
Carl Thomas Electric
{datetime.now().strftime('%B %d, %Y')}
{'=' * 60}

BILL TO:
{customer['name']}
Email: {customer['email']}

INVOICE #{}
DUE DATE: {} + 30 days

{{}}
----------------------------------------
Total Due: ${}.{:02f}
----------------------------------------

Status: {}
""".format(
        invoice["invoice_number"],
        invoice["created_at"].date(),
        invoice["description"]),
        invoice["amount"]
    )
    
    return template

# Interactive console mode
if __name__ == "__main__":
    print("=" * 70)
    print("Carl Thomas Electric - Invoicing Portal")
    print("=" * 70)
    print()
    
    while True:
        print("\n📋 Available Commands:")
        print("  customers      - List all customers")
        print("  invoices       - Show all invoices")  
        print("  estimates      - Show all estimates")
        print("  quit           - Exit console")
        print()
            
        try:
            command = input("\n> ").strip().lower()
                
            if command == "quit":
                print("👋 Goodbye!")
                break
            elif command == "customers":
                for c in customers.values():
                    print(f"CUST-{c['id']} | {c['name']} | {c['email']}")
                        
            elif command.startswith("create_invoice"):
                remaining = command.replace("create_invoice ", "").rstrip()
                if "'" in remaining:
                    parts = remaining.split("'")
                    if len(parts) >= 2:
                        cust_id = int(parts[0].strip())
                        desc = parts[1]
                        result = create_invoice(cust_id, desc)
                        print(result)
                        break
                            
            elif command.startswith("create_estimate"):
                remaining = command.replace("create_estimate ", "").rstrip()
                if not remaining:
                    print("  Use: create_estimate <cust_id> 'description' [amount]")
                else:
                    parts = remaining.replace("'", '"').split('"')
                    cust_id = int(parts[0].strip())
                    desc = parts[1] if len(parts) > 1 else ""
                    amount = float(parts[2]) if len(parts) > 2 else 500.0
                    result = create_estimate(cust_id, desc, total_amount=amount)
                    print(result)
                        
            elif command == "invoices":
                items = list_invoices()
                for item in items:
                    status_emoji = "🟠 Pending" if item.get("status")=="pending" else \
                                   "✅ Sent/Paid" if item.get("status")!="pending" else "?"
                    print(f"#{item['id']}.  {item['description']}  | ${item['amount']:,.2f}  {status_emoji}")
                        
            elif command == "estimates":   
                items = list_estimates()
                for item in items:
                    status_emoji = "🟢 Draft/Open" if item.get("status")=="draft" else \
                                   "✅ Completed/Closed" if item.get("status")!="draft" else "?"
                    print(f"#{item['id']}.  {item['description']}  | ${item['amount']:,.2f}  {status_emoji}")
                    
        except ValueError as e:
            continue
        except (EOFError, KeyboardInterrupt):
            break

    print()
    print("👋 Goodbye!")
