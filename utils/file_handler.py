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

