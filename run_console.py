"""
Carl Thomas Electric - Console Application for Invoicing Portal
Uses only Python standard library - no dependencies needed!
"""
from datetime import datetime

# Customer database
customers = {
    1: {"id": 1, "name": "John Smith Company", "email": "john@smith.com"},
    2: {"id": 2, "name": "Mary Johnson Properties", "email": "mary@mproperties.com"}
}

# Invoice tracking (in-memory for demo)
invoices = [
    {"invoice_number": "INV-101", "customer_id": 1, "description": "Electrical work on residential property", 
     "amount": 2500.00, "status": "sent"}
]

# Estimates tracking  
estimates = [
    {"estimate_number": "EST-1", "customer_id": 1, "description": "EV charging station installation", "amount": 3200.00}
]

print("=" * 70)
print("Carl Thomas Electric - Invoicing Portal")
print("=" * 70)
print()
print("Available commands (type 'help' for full list):")
print("  customers      - List all customers")
print("  invoices       - Show all invoices")  
print("  estimates      - Show all estimates")
print("  new_invoice <id> 'description' [amount]  Create invoice")
print("  new_estimate   <id> 'description' [amount] Create estimate")
print("  convert_est #    Convert estimate # to invoice")
print("  quit             Exit console")
print()

while True:
    command = input(f"\nCarlThomasElectric({datetime.now().strftime('%H:%M')})> ").strip().lower()
    
    if command == "quit":
        print("\nQuitting... 👋")
        break
        
    elif command == "" or command.isspace():
        continue
    
    elif command in ["help", "?"]:
        print("""Commands:
  customers         List all registered customers with contact info
  invoices          View all created invoices
  estimates         View active and completed estimates
  new_invoice <id> 'description' [amount] - Create a new invoice
  new_estimate   <id> 'description' [amount] - Create estimate
  convert_est #     Convert an estimate to an invoice
  quit              Exit the application
        
Examples:
  customers
  invoices
  new_invoice 1 Work on electrical panel upgrade $4500
  new_estimate 2 Install smart thermostat system $980
""")
        continue
        
    elif command.startswith("customers"):
        print("\n--- CUSTOMERS ---")
        for cid, c in customers.items():
            print(f"CUSTOMER #{cid}")
            print(f"  Name : {c['name']}")
            print(f"  Email: {c['email']}")
            
    elif command.startswith("invoices"):
        print("\n--- INVOICES ---")
        if not invoices:
            print("No invoices created yet.")
        else:
            for inv in invoices:
                status = "🟠 Pending" if inv["status"] == "pending" else "✅ Sent/Paid"
                cid_client_id = inv["customer_id"]
                print(f"\nInvoice #{inv['invoice_number']}")
                print(f"  Customer: CUST-{cid_client_id}")  
                print(f"  Description: {inv['description']}")
                print(f"  Amount: ${inv['amount']:,.2f}")
                print(f"  Status: {status}")
                
    elif command.startswith("estimates"):
        print("\n--- ESTIMATES ---")
        if not estimates:
            print("No estimates created yet.")  
        else:
            for est in estimates:
                status = "🟢 Open/Active" if est["status"] == "draft" else "✅ Completed" 
                print(f"\nEstimate #{est['estimate_number']}")
                print(f"  Customer: cust_{est['customer_id']}>")
                print(f"  Description: {est['description']}")
                print(f"  Amount estimate ${est['amount']:,.2f}")
                print(f"  Status: {status}")
                
    elif command.startswith("new_invoice"):
        parts = command.replace("new_invoice ", "").split()
        if len(parts) >= 2:
            try:
                cust_id = int(parts[0].strip())
                desc = f"{' '.join(parts[1:-1])}" if "-" in parts[-1] else " ".join(parts[1:-1])
                amount = float(parts[-1].replace("$","").replace(",","")) if len(parts) > 3 else 1000.0
                
                inv_num = f"INV-{100 + len(invoices)}"
                new_inv = {
                    "invoice_number": inv_num,
                    "customer_id": cust_id,
                    "description": desc,
                    "amount": amount,
                    "status": "pending",
                    "created_at": datetime.now()
                }
                invoices.append(new_inv)
                print(f"\n✅ Invoice created: {inv_num}")
                print(f   Amount: ${amount:,.2f}")
                
            except (ValueError, IndexError):
                print("Invalid format. Use: new_invoice <customer_id> 'description' [amount]")
                
    elif command.startswith("new_estimate"):
        parts = command.replace("new_estimate ", "").split()
        if len(parts) >= 2:
            try:
                cust_id = int(parts[0].strip())
                desc = f"{' '.join(parts[1:-1])}" 
                amount = float(parts[-1].replace("$","").replace(",","")) if len(parts) > 3 else 500.0
                
                est_num = f"EST-{1 + len(estimates)}"
                new_est = {
                    "estimate_number": est_num,
                    "customer_id": cust_id, 
                    "description": desc,
                    "amount": amount,
                    "status": "draft",
                    "created_at": datetime.now()
                }
                estimates.append(new_est)
                print(f"\n✅ Estimate created: {est_num}")
                print(f"  Amount estimate ${amount:,.2f}")
                
            except (ValueError, IndexError):
                print("Invalid format. Use: new_estimate <customer_id> 'description' [amount]")
                
    elif command.startswith("convert_est"):
        try:
            est_num = int(command.split()[2])
            
            # Find and mark estimate as completed  
            for est in estimates:
                if est["estimate_number"] == f"EST-{est_num}":
                    est["status"] = "completed"
                    
                    # Create invoice
                    inv_num = f"INV-{100 + len(invoices)}"
                    new_inv = {
                        "invoice_number": inv_num, 
                        "customer_id": est["customer_id"],
                        "description": f"{est['description']} (CONVERTED FROM ESTIMATE #{est_num})",
                        "amount": est["amount"],
                        "status": "pending", 
                        "converted_from": est_num
                    }
                    invoices.append(new_inv)
                    
                    print(f"\n✅ Converted estimate #{est_num} to invoice")  
                    print(f   New Invoice: {inv_num}")
                    print(f  Amount: ${est['amount']:,.2f}")
                    break
                    
        except (IndexError, ValueError):
            print("Invalid command. Use: convert_est <estimate_number>")
            
print()
