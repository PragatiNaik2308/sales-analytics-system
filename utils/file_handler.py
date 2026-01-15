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
            if len(part_data) !=8:
                continue

            transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = part_data
            
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

