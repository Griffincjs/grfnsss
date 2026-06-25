import requests
import random
from datetime import datetime, timedelta

# API URL (The same one your dashboard uses)
URL = "http://127.0.0.1:8000/data/upload"

# Clothing categories and sample SKUs
PRODUCTS = {
    "T-Shirts": ["TSHIRT-BLK-M", "TSHIRT-WHT-L", "TSHIRT-RED-S"],
    "Pants": ["JEANS-BLU-32", "CHINO-KHK-34", "JOGGER-GRY-M"],
    "Outerwear": ["HOODIE-NVY-L", "JACKET-LTH-XL", "VEST-BLK-M"]
}

def generate_fake_sales(num_records=50):
    sales_data = []
    today = datetime.now()

    for _ in range(num_records):
        # Pick a random category and then a random SKU from that category
        cat = random.choice(list(PRODUCTS.keys()))
        sku = random.choice(PRODUCTS[cat])
        
        # Randomize date (within the last 30 days), quantity, and price
        random_days = random.randint(0, 30)
        sale_date = (today - timedelta(days=random_days)).strftime("%Y-%m-%d")
        
        record = {
            "date": sale_date,
            "sku": sku,
            "category": cat,
            "quantity_sold": random.randint(1, 10),
            "price": random.choice([19.99, 29.99, 49.99, 89.99])
        }
        sales_data.append(record)

    # Send it to the API
    response = requests.post(URL, json=sales_data)
    if response.status_code == 200:
        print(f"✅ Success! {response.json()['message']}")
    else:
        print(f"❌ Failed! {response.text}")

if __name__ == "__main__":
    generate_fake_sales(100) # Let's generate 100 sales