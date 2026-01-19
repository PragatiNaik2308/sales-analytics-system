import requests

def fetch_all_products():
    try:
        response = requests.get('https://dummyjson.com/products?limit=100')

        if response.status_code != 200:
            raise ConnectionError(f"API returned status code {response.status_code}")
        
        data = response.json()
        products = data['products']

        result = []
        for product in products:
            result.append({
                "id": product.get("id"),
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "price": product.get("price"),
                "rating": product.get("rating")
            })

        print(f"Successfully fetched {len(result)} products from API")
        return result

    except requests.exceptions.ConnectionError:
        print("FAILURE: Unable to connect to DummyJSON API")
        return []

    except requests.exceptions.Timeout:
        print("FAILURE: API request timed out")
        return []

    except Exception as e:
        print(f"FAILURE: Unexpected error occurred → {e}")
        return []


def create_product_mapping(api_products):
    product_mapping = {}

    for product in api_products:
        try:
            product_id = product['id']
            
            # Skip invalid product records
            if product_id is None:
                continue
            
            product_mapping[product_id] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"), 
                "rating": product.get("rating")
            }

        except (TypeError, AttributeError):
            continue # Skip malformed product entries safely

    return product_mapping


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]
    try:
        # Open the file in write mode
        with open(filename, "w") as file:
            # Write header
            file.write("|".join(headers) + "\n")

            for transaction in enriched_transactions:
                row = []
                for field in headers:
                    value = transaction.get(field)
                    row.append("" if value is None else str(value))
                file.write("|".join(row) + "\n")

        print(f"SUCCESS: Enriched data saved to {filename}")

    except IOError as e:
        print(f"ERROR: Failed to write enriched file → {e}")


def enrich_sales_data(transactions, product_mapping):
    enrich_transactions = []

    for transaction in transactions:
        enrich_trans = transaction.copy()

        product_id = transaction.get("ProductID", "")
        # Extract numeric product ID
        numeric_prouduct_id = int(product_id[1:]) if product_id.startswith("P") else None

        api_product = product_mapping.get(numeric_prouduct_id)

        try: 
            if api_product:
                enrich_trans["API_Category"] = api_product.get("category")
                enrich_trans["API_Brand"] = api_product.get("brand")
                enrich_trans["API_Rating"] = api_product.get("rating")
                enrich_trans["API_Match"] = True
            else:
                enrich_trans["API_Category"] = None
                enrich_trans["API_Brand"] = None
                enrich_trans["API_Rating"] = None
                enrich_trans["API_Match"] = False
                
        except Exception:
            # Graceful failure
            enrich_trans["API_Category"] = None
            enrich_trans["API_Brand"] = None
            enrich_trans["API_Rating"] = None
            enrich_trans["API_Match"] = False

        enrich_transactions.append(enrich_trans)

    save_enriched_data(enrich_transactions)

    






