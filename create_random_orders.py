import requests
import random
from datetime import datetime, timedelta
import faker

fake = faker.Faker()

BASE_URL = 'http://localhost:8000/api/orders/'
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Origin": "http://localhost:3000",
    "Connection": "keep-alive",
    "Referer": "http://localhost:3000/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=0"
}

def random_date(start_year=2023, end_year=2025):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).date().isoformat()

def random_price():
    return round(random.uniform(1.0, 100.00), 2)  # price >= 1.00 for realism

def create_order(customer_name, description, date_str):
    payload = {
        "customer_name": customer_name,
        "description": description,
        "date": date_str
    }

    response = requests.post(BASE_URL, headers=HEADERS, json=payload)

    if response.status_code == 201:
        return response.json().get('id')
    else:
        print(f"[!] Failed to create order: {response.status_code}, {response.text}")
        return None

def update_order_with_products(order_id, customer_name, description, date_str, products):
    payload = {
        "customer_name": customer_name,
        "description": description,
        "date": date_str,
        "products": products,
        "products_to_delete": [],
        "version": 0
    }

    url = f"{BASE_URL}{order_id}/"
    response = requests.put(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        print(f"[+] Order {order_id} updated with {len(products)} products.")
    else:
        print(f"[!] Failed to update order {order_id}: {response.status_code}, {response.text}")

def main():
    for i in range(1000):
        customer_name = fake.name()
        description = fake.sentence(nb_words=6)
        date_str = random_date()

        order_id = create_order(customer_name, description, date_str)
        if order_id is None:
            continue

        num_products = random.randint(1, 10)
        products = [
            {
                "id": None,
                "name": fake.word().capitalize(),
                "price": random_price()
            }
            for _ in range(num_products)
        ]

        update_order_with_products(order_id, customer_name, description, date_str, products)

if __name__ == "__main__":
    main()
