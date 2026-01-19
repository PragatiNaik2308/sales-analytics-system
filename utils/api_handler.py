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

