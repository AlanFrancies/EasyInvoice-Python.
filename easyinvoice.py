from html import escape
from pathlib import Path
import webbrowser

print("=== EasyInvoice ===")

business = input("Your business name: ").strip()
customer = input("Customer name: ").strip()
invoice_number = input("Invoice number: ").strip()

if not business or not customer or not invoice_number:
    print("Business, customer, and invoice number are required.")
    raise SystemExit

items = []

while True:
    name = input("Item or service name (blank to finish): ").strip()
    if not name:
        break

    try:
        quantity = float(input("Quantity: "))
        price = float(input("Price per unit (INR): "))

        if quantity <= 0 or price < 0:
            print("Quantity must be positive; price cannot be negative.")
            continue

        items.append((name, quantity, price))
    except ValueError:
        print("Please enter valid numbers.")
        
if not items:
    print("No items entered. Please run the program again.")
    raise SystemExit

total = sum(qty * price for _, qty, price in items)

rows = ""
for name, qty, price in items:
    rows += (
        "<tr><td>" + escape(name) + "</td>"
        f"<td>{qty:g}</td>"
        f"<td>₹{price:.2f}</td>"
        f"<td>₹{qty * price:.2f}</td></tr>"
    )

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Invoice {escape(invoice_number)}</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 800px;
       margin: 40px auto; padding: 20px; color: #222; }}
h1 {{ color: #2457a7; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 24px; }}
th, td {{ padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }}
.total {{ text-align: right; font-size: 22px; margin-top: 24px; }}
button {{ padding: 12px 18px; cursor: pointer; }}
@media print {{ button {{ display: none; }} body {{ margin: 0; }} }}
</style>
</head>
<body>
<h1>INVOICE</h1>
<p><strong>From:</strong> {escape(business)}</p>
<p><strong>Bill to:</strong> {escape(customer)}</p>
<p><strong>Invoice number:</strong> {escape(invoice_number)}</p>
<table>
<thead><tr><th>Item</th><th>Qty</th>
<th>Unit price</th><th>Amount</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<div class="total"><strong>Total: ₹{total:.2f}</strong></div>
<p>Thank you for your business!</p>
<button onclick="window.print()">Print / Save as PDF</button>
</body>
</html>"""

output = Path("invoice.html").resolve()
output.write_text(html, encoding="utf-8")
webbrowser.open(output.as_uri())

print(f"Invoice total: ₹{total:.2f}")
print(f"Invoice saved to: {output}")
