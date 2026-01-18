def calculate_total_revenue(transactions):
    total_revenue = 0.0

    for transaction in transactions:
        try:
            quantity = transaction.get("Quantity", 0)
            unit_price = transaction.get("UnitPrice", 0.0)
            total_revenue += quantity * unit_price

        except (TypeError, ValueError):
            # Skip malformed records safely
            continue

    return float(total_revenue)


def region_wise_sales(transactions):
    sales_summary = {}
    overall_total = 0.00

    # Calculate total sales and transaction count per region
    for transaction in transactions:
        try:
            region = transaction['Region']
            amount = transaction['Quantity'] * transaction['UnitPrice']
            overall_total += amount

            if region not in sales_summary:
                sales_summary[region] = {
                    "total_sales": 0.0,
                    "transaction_count": 0
                }

            sales_summary[region]["total_sales"] += amount 
            sales_summary[region]["transaction_count"] += 1
        
        except (ValueError, TypeError):
            # Skip malformed records safely
            continue

    # Calculate percentage contribution
    for region in sales_summary:
        sales_summary[region]["percentage"] = (sales_summary[region]["total_sales"] / overall_total) * 100

    # Sort by total_sales (descending)
    sorted_region_summary = dict(
        sorted(
        sales_summary.items(),
        key=lambda item: item[1]["total_sales"],
        reverse=True
        )
    )

    return sorted_region_summary


def top_selling_products(transactions, n=5):
    product_summary = {}

    # Aggregate quantity and revenue per product
    for transaction in transactions:
        try:
            productName = transaction['ProductName']
            quantity = transaction['Quantity']
            amount = transaction['Quantity'] * transaction['UnitPrice']
            
            if productName not in product_summary:
                product_summary[productName] = {
                    "total_quantity": 0,
                    "total_revenue": 0.0
                }

            product_summary[productName]["total_quantity"] += quantity
            product_summary[productName]["total_revenue"] += amount

        except (ValueError, TypeError):
            # Skip malformed records safely
            continue
    
    # Convert dictionary to list of tuples
    product_list  = [
        (productName,
         details["total_quantity"],
         details["total_revenue"], )
        for productName, details in product_summary.items()
    ]

    # Sort by TotalQuantity (descending)
    product_list.sort(key=lambda item: item[1], reverse=True)

    # Return top n products
    return product_list[:n]


def customer_analysis(transactions):
    customer_summary = {}

    # Aggregate total amount and purchase count per customer
    for transaction in transactions:
        try:
            customer = transaction['CustomerID']
            amount = transaction['Quantity'] * transaction['UnitPrice']
            productName = transaction['ProductName']

            if customer not in customer_summary:
                    customer_summary[customer] = {
                        "total_spent": 0.0,
                        "purchase_count": 0,
                        "products_bought": set()
                    }

            customer_summary[customer]["total_spent"] += amount
            customer_summary[customer]["purchase_count"] += 1
            customer_summary[customer]["products_bought"].add(productName)

        except (ValueError, TypeError):
            # Skip malformed records safely
            continue
    
    # Calculate averages order value & convert sets → lists
    for customer in customer_summary:
        customer_summary[customer]["avg_order_value"] = customer_summary[customer]["total_spent"] / customer_summary[customer]["purchase_count"]

    # Sort by total_spent (descending)
    sorted_customer_summary = dict(
        sorted(
        customer_summary.items(),
        key=lambda item: item[1]["total_spent"],
        reverse=True
        )
    )

    return sorted_customer_summary


def daily_sales_trend(transactions):
    daily_summary = {}

    # Aggregate daily revenue, daily transactions count per day
    for transaction in transactions:
        try:
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

        except (ValueError, TypeError):
            # Skip malformed records safely
            continue

    # unique customers count 
    for date in daily_summary:
        daily_summary[date]["unique_customers"] = len(daily_summary[date]["customers"])
        del daily_summary[date]["customers"]

    # Sort chronologically by date
    sorted_daily_summary = dict(sorted(daily_summary.items()))

    return sorted_daily_summary


def find_peak_sales_day(transactions):
    daily_sales_summary = {}

    # Aggregate daily revenue, daily transactions count per day
    for transaction in transactions:
        try:
            date = transaction['Date']
            amount = transaction['Quantity'] * transaction['UnitPrice']

            if date not in daily_sales_summary:
                    daily_sales_summary[date] = {
                        "revenue": 0.0,
                        "transaction_count": 0,
                    }

            daily_sales_summary[date]["revenue"] += amount
            daily_sales_summary[date]["transaction_count"] += 1

        except (ValueError, TypeError):
            # Skip malformed records safely
            continue
    
    # Peak day sales
    peak_date = None
    peak_revenue = 0
    peak_transcation = 0

    for date in daily_sales_summary:
        if daily_sales_summary[date]["revenue"] > peak_revenue:
            peak_revenue = daily_sales_summary[date]["revenue"]
            peak_date = date
            peak_transcation = daily_sales_summary[date]["transaction_count"]

    return (peak_date, peak_revenue, peak_transcation)


def low_performing_products(transactions, threshold=10):
    product_summary = {}

    # Aggregate quantity and revenue per product
    for transaction in transactions:
        try:
            productName = transaction['ProductName']
            quantity = transaction['Quantity']
            amount = transaction['Quantity'] * transaction['UnitPrice']
            
            if productName not in product_summary:
                product_summary[productName] = {
                    "total_quantity": 0,
                    "total_revenue": 0.0
                }

            product_summary[productName]["total_quantity"] += quantity
            product_summary[productName]["total_revenue"] += amount

        except (ValueError, TypeError):
            # Skip malformed records safely
            continue
    
    # Convert dictionary to list of tuples
    low_products  = [
        (productName,
         details["total_quantity"],
         details["total_revenue"], )
        for productName, details in product_summary.items()
        if details['total_quantity'] < threshold
    ]

    # Sort by TotalQuantity (ascending)
    low_products.sort(key=lambda item: item[1])

    return low_products


    
    


        



    






