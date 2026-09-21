"""Carl Thomas Electric - Console Application 
No dependencies required! Uses only Python standard library."""
from datetime import datetime

# Customers
customers = {1: {"id": 1, "name": "John Smith Company", "email": "john@smith.com"}, 
              2: {"id": 2, "name": "Mary Johnson Properties", "email": "mary@mproperties.com"}}

# Data stores
invoices = []
estimates = []

print("=" * 60)
print("Carl Thomas Electric - Invoicing Portal")
print("=" * 60)
while True:
    cmd = input(f"\nCommand> ").strip().lower()
    
    if cmd == "quit":
        break
    elif cmd == "" or cmd.isspace():
        continue      
    elif cmd in ["help", "?"]:
        print("Commands: customers|invoices|estimates|new_invoice <id>'desc' [amt]|quit")
        print("          new_estimate <id>'desc' [amt]<convert_est # >")
        continue
        
    elif cmd == "customers":
        for c in customers.values():
            print(f"{c['name']} ({c['email']})")
            
    elif cmd == "invoices":
        if not invoices:
            print("No invoices yet.")
        else:
            for inv in invoices:  
                print(f"Invoice #{inv['invoice_number']} - ${inv['amount']:,.2f} - {inv['status']}")
                
    elif cmd == "estimates":  
        if not estimates:
            print("No estimates yet.")
        else:
            for est in estimates:
                print(f"Estimate #{est['estimate_number']} - ${est['amount']:,.2f} - {est['status']}")

print()
