import requests
from datetime import datetime

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


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    # Overall Summary Metrics
    total_transactions = len(transactions)
    total_revenue = sum(transaction['Quantity'] * transaction['UnitPrice'] for transaction in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0
    dates= sorted(transaction['Date'] for transaction in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else None

    # Region-Wise Performance Metrics
    region_stats = {}

    for transaction in transactions:
        region = transaction['Region']
        amount = transaction['Quantity'] * transaction['UnitPrice']

        if region not in region_stats:
            region_stats[region] = {'total_sales': 0.0, 'transaction_count': 0}

        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1

    region_wise_summary = []
    for region, data in region_stats.items():
        percentage = (data['total_sales'] / total_revenue) * 100 if total_revenue else 0
        region_wise_summary.append((region, data['total_sales'], percentage, data['transaction_count']))

    region_wise_summary.sort(key=lambda x: x[1], reverse=True)

    # Top 5 Products Metrics 
    product_stats = {}

    for transaction in transactions:
            productName = transaction['ProductName']
            quantity = transaction['Quantity']
            amount = transaction['Quantity'] * transaction['UnitPrice']
            
            if productName not in product_stats:
                product_stats[productName] = {
                    "total_quantity": 0,
                    "total_revenue": 0.0
                }

            product_stats[productName]["total_quantity"] += quantity
            product_stats[productName]["total_revenue"] += amount

    top_products = sorted(
        product_stats.items(),
        key=lambda x: x[1]['total_quantity'],
        reverse=True
    )[:5]

    # Top 5 Customer Metrics
    customer_summary = {}

    for transaction in transactions:
        customer = transaction['CustomerID']
        amount = transaction['Quantity'] * transaction['UnitPrice']
        productName = transaction['ProductName']

        if customer not in customer_summary:
                customer_summary[customer] = {
                    "total_spent": 0.0,
                    "purchase_count": 0,
                }

        customer_summary[customer]["total_spent"] += amount
        customer_summary[customer]["purchase_count"] += 1

    top_customers = sorted(
        customer_summary.items(),
        key=lambda x: x[1]['total_spent'],
        reverse=True
    )[:5]

    # Daily Sales Trend Metrics
    daily_summary = {}

    for transaction in transactions:
        date = transaction['Date']
        amount = transaction['Quantity'] * transaction['UnitPrice']
        customer = transaction['CustomerID']

        if date not in daily_summary:
                daily_summary[date] = {
                    "revenue": 0.0,
                    "transaction_count": 0,
                    "customers": set(),
                }

        daily_summary[date]["revenue"] += amount
        daily_summary[date]["transaction_count"] += 1
        daily_summary[date]["customers"].add(customer)

    for date in daily_summary:
        daily_summary[date]["unique_customers"] = len(daily_summary[date]["customers"])
        del daily_summary[date]["customers"]

    daily_sales_trend = sorted(daily_summary.items())

    # Product Performance Analysis
    # Best selling day
    best_selling_day = max(sorted(daily_summary.items(), key=lambda item: item[1]["revenue"]))

    # Low performing products 
    # Since threshold for detrming the low performing products is not given, 
    # Therefore, I condidered last 5 products as low performing products
    low_performing_products = sorted(
        product_stats.items(),
        key=lambda x: x[1]['total_quantity']
    )[:5]

    # Average transaction value per region
    avg_value_per_region = {}
    for region in region_stats:
        avg_value_per_region[region] = region_stats[region]["total_sales"] / region_stats[region]["transaction_count"]

    # API ENRICHMENT SUMMARY
    # Total products enriched count and List of products that couldn't be enriched
    enriched_count = 0
    failed_products = set()
    for transaction in enriched_transactions:
        if transaction["API_Match"] == True:
            enriched_count += 1
        else: failed_products.add(transaction["ProductName"])
    
    # Success rate percentage
    success_rate = (enriched_count / len(enriched_transactions) ) * 100 if enriched_transactions else 0

    # WRITE REPORT
    try:
        with open(output_file, 'w')as file:
            # HEADER
            file.write("=" * 50 + "\n")
            file.write("       SALES ANALYTICS REPORT\n")
            file.write(f"    Generated: {datetime.now()}\n")
            file.write(f"    Records Processed: {total_transactions}\n")
            file.write("=" * 50 + "\n\n")

            # OVERALL SUMMARY
            file.write("OVERALL SUMMARY\n")
            file.write("-" * 50 + "\n")
            file.write(f"Total Revenue:        {total_revenue}\n")
            file.write(f"Total Transactions:   {total_transactions}\n")
            file.write(f"Average Order Value:  {avg_order_value}\n")
            file.write(f"Date Range:           {date_range}\n\n")

            # REGION-WISE PERFORMANCE
            file.write("REGION-WISE PERFORMANCE\n")
            file.write("-" * 50 + "\n")
            file.write(f"{'Region':10}{'Sales':15}{'% of Total':12}{'Txns'}\n")
            for r, s, p, c in region_wise_summary:
                file.write(f"{r:10}{s:9,.0f}{p:11.2f}%{c:8}\n")
            file.write("\n")

            # TOP 5 PRODUCTS
            file.write("TOP 5 PRODUCTS\n")
            file.write("-" * 50 + "\n")
            file.write(f"{'Rank':6}{'Product Name':<20}{'Quantity Sold':>15}{'Revenue':>15}\n")
            for i, (p, d) in enumerate(top_products, 1):
                file.write(f"{i:<6} {p:<20}{d['total_quantity']:>8} {d['total_revenue']:>20,.2f}\n")
            file.write("\n")

            # TOP 5 CUSTOMERS
            file.write("TOP 5 CUSTOMERS\n")
            file.write("-" * 50 + "\n")
            file.write(f"{'Rank':6}{'Customer ID':<20}{'Total Spent':>8}{'Order Count':>15}\n")
            for i, (p, d) in enumerate(top_customers, 1):
                file.write(f"{i:<6} {p:<20}{d['total_spent']:>8} {d['purchase_count']:>12}\n")
            file.write("\n")
            
            # DAILY SALES TREND
            file.write("DAILY SALES TREND\n")
            file.write("-" * 50 + "\n")
            file.write(f"{'Date':<15}{'Revenue':>8}{'Transactions':>15}{'Unique Customers':>20}\n")
            for i, (p, d) in enumerate(daily_sales_trend, 1):
                file.write(f"{p:<15} {d['revenue']:>8} {d['transaction_count']:>8}{d['unique_customers']:>16}\n")
            file.write("\n")

            # PRODUCT PERFORMANCE ANALYSIS
            file.write("PRODUCT PERFORMANCE ANALYSIS\n")
            file.write("-" * 50 + "\n")
            file.write(f"Best Selling Day: {best_selling_day[0]} (Revenue: {best_selling_day[1]['revenue']:,.2f})\n\n")
            file.write(f"Low performing products:\n")
            file.write(f"{'Rank':6}{'Product Name':<20}{'Quantity Sold':>15}{'Revenue':>15}\n")
            for i, (p, d) in enumerate(low_performing_products, 1):
                file.write(f"{i:<6} {p:<20}{d['total_quantity']:>8} {d['total_revenue']:>20,.2f}\n")
            file.write("\n")
            file.write(f"Average transaction value per region:\n")
            for r, a in avg_value_per_region.items():
                file.write(f"{r}: {a:,.2f}\n")
            file.write("\n")

            # API ENRICHMENT SUMMARY
            file.write("API ENRICHMENT SUMMARY\n")
            file.write("-" * 50 + "\n")
            file.write(f"Total products enriched: {enriched_count}\n")
            file.write(f"Success rate percentage: {success_rate:.2f}\n")
            file.write(f"List of products that couldn't be enriched:\n")
            for p in failed_products:
                file.write(f" - {p}\n")
        print(f"SUCCESS: Sales report generated at {output_file}")
    except IOError as e:
        print(f"ERROR: Failed to write sales report file → {e}")



    






