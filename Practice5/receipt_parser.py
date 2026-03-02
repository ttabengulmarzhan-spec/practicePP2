import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Extract prices
prices = re.findall(r'\d[\d\s]*,\d{2}', text)

# Extract product names
products = re.findall(r'\d+\.\n(.+)', text)

# Extract total
total = re.search(r'ИТОГО:\n([\d\s]+,\d{2})', text)
total_amount = total.group(1) if total else None

# Extract datetime
datetime_match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})', text)
datetime_value = datetime_match.group(1) if datetime_match else None

# Extract payment method
payment = re.search(r'(Банковская карта)', text)
payment_method = payment.group(1) if payment else None

data = {
    "products": products,
    "prices": prices,
    "total": total_amount,
    "datetime": datetime_value,
    "payment_method": payment_method
}

print(json.dumps(data, ensure_ascii=False, indent=4))
