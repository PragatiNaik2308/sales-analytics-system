def read_sales_data(filename):
    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            with open(filename, "r", encoding=encoding) as file:
                lines = file.readlines()
                break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File not found -> {filename}")
            return []

    else:
        print("Error: Unable to read file with supported encodings")
        return []
    
    cleaned_lines = []

    for i, line in enumerate(lines):
        line = line.strip()

        # Skip header
        if i == 0:
            continue

        # Skip empty lines
        if not line:
            continue

        cleaned_lines.append(line)
    
    return cleaned_lines


def parse_transactions(raw_lines):
    parsed_data = []

    for line_no, line in enumerate(raw_lines, start=1):
        try:
            # Split by pipe delimiter
            part_data = line.split('|')

            # Skip rows with incorrect number of fields
            if len(part_data) != 8:
                continue

            transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = part_data
            
            # Skip rows with missing field value
            if not all([transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region]):
                continue
            
            #  Handle Product Name (remove commas) and numeric fields ()
            record = {
                "TransactionID": transaction_id.strip(),
                "Date": date.strip(),
                "ProductID": product_id.strip(),
                "ProductName": product_name.replace(",", " ").strip(),
                "Quantity": int(quantity.replace(",", "").strip()), #convert to int 
                "UnitPrice": float(unit_price.replace(",", "").strip()), #convert to float
                "CustomerID": customer_id.strip(),
                "Region": region.strip()
            }

            parsed_data.append(record)

        except Exception as e:
            print(f"Line {line_no} skipped due to unexpected error: {e}")

    return parsed_data


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    regions = set()
    amounts = []

    valid_transactions = []
    invalid_count = 0
    summary = {
        'total_input': len(transactions),
        'invalid': 0,
        'filtered_by_region': 0,
        'filtered_by_amount': 0,
        'final_count': 0
    }

    # Display available regions and transaction amount range
    for transaction in transactions:
        if "Region" in transaction:
            regions.add(transaction['Region'])
        if "Quantity" in transaction and "UnitPrice" in transaction:
            amounts.append(transaction['Quantity'] * transaction['UnitPrice'])

    print("Available Regions:", sorted(regions))

    if amounts:
        print(f"Transaction Amount Range: {min(amounts)} to {max(amounts)}")

    # Validation of records
    for transaction in transactions:
        try:
            if transaction['Quantity'] <= 0:
                raise ValueError("Invalid Quantity")
            if transaction['UnitPrice'] <= 0:
                raise ValueError("Invalid Unit Price")
            # Skip rows with missing field value
            if not all(["TransactionID", "Date", "ProductID", "ProductName", "Quantity", "UnitPrice", "CustomerID", "Region"]):
                raise ValueError("Missing required field")
            if not transaction['TransactionID'].startswith('T'):
                raise ValueError("Invalid TransactionID")
            if not transaction['ProductID'].startswith('P'):
                 raise ValueError("Invalid ProductID")
            if not transaction['CustomerID'].startswith('C'): 
                raise ValueError("Invalid CustomerID")
            valid_transactions.append(transaction)
            
        except:
            invalid_count += 1

    summary['invalid'] = invalid_count

    print(f"After validation: {len(valid_transactions)}")

    # Filter by Region
    if region is not None:
        before = len(valid_transactions)
        valid_transactions = [transaction for transaction in valid_transactions if transaction['Region'] == region.capitalize()]
        summary['filtered_by_region'] = before - len(valid_transactions)

    print(f"After region filter ({region}): {len(valid_transactions)}")

    # Filter by amount
    if min_amount is not None and max_amount is not None:
        before = len(valid_transactions)
        amount_filter = []
        for transaction in valid_transactions:
            amount = transaction['Quantity'] * transaction['UnitPrice']

            if amount is not None and amount < min_amount:
                continue
            if amount is not None and amount > max_amount:
                continue

            amount_filter.append(transaction)
        valid_transactions = amount_filter
        summary["filtered_by_amount"] = before - len(valid_transactions)

    print(f"After amount filter ({min_amount}-{max_amount}): {len(valid_transactions)}")

    summary["final_count"] = len(transactions) - invalid_count - summary['filtered_by_region'] - summary["filtered_by_amount"]
    return valid_transactions, invalid_count, summary
