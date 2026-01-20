from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import calculate_total_revenue, region_wise_sales, top_selling_products,customer_analysis, daily_sales_trend, find_peak_sales_day, low_performing_products
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data, generate_sales_report

def main():
    try:
        # 1. Print welcome message
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 2. Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        if not raw_lines:
            print("✗ Failed to read sales data")
            return
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        #3. Parse and clean transactions
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        if not transactions:
            print("✗ Failed to parse and clean data")
            return
        print(f"✓ Successfully parsed {len(transactions)} transactions")

        # 4. Display filter options to user
        print("\n[3/10] Filter Options Available:")
        region = sorted({transaction['Region'] for transaction in transactions})
        amount = [transaction['Quantity'] * transaction['UnitPrice'] for transaction in transactions]
        print(f"Regions: {region}")
        print(f"Amount Range: {min(amount):,.0f} - {max(amount):,.0f}")

        apply_filter = input("Do you want to filter data? (y/n): ").strip().lower()

        # 5. If yes, ask for filter criteria and apply
        region = min_amount = max_amount = None
        if apply_filter == "y":
            region = input("Enter region (or press Enter to skip): ").strip() or None
            if input("Do you want to apply filter by amount? (y/n): ").lower()  == "y":
                min_amount = float(input("Enter minimum amount: "))
                max_amount = float(input("Enter maximum amount: "))
            
        # 6. Validate transactions
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(transactions, region=region, min_amount=min_amount, max_amount=max_amount)
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # 7. Display validation summary
        print("Validation Summary:")
        print(f"  Total Records   : {summary['total_input']}")
        print(f"  Invalid Record Counts: {summary['invalid']}")
        print(f"  Filtered By Region: {summary['filtered_by_region']}")
        print(f"  Filtered By Amount: {summary['filtered_by_amount']}")
        print(f"  Valid Records   : {summary['final_count']}")

        #  8. Perform all data analyses 
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_transactions)
        region_wise_sales(valid_transactions)
        top_selling_products(valid_transactions)
        customer_analysis(valid_transactions)
        daily_sales_trend(valid_transactions)
        find_peak_sales_day(valid_transactions)
        low_performing_products(valid_transactions)
        print("✓ Analysis complete")

        # 9. Fetch products from API
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # 10. Enrich sales data with API info
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
        success_rate = (enriched_count / len(valid_transactions)) * 100 if valid_transactions else 0
        print(f"✓ Enriched {enriched_count}/{len(valid_transactions)} transactions ({success_rate:.1f}%)")

        # 11. Save enriched data to file
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print("✓ Saved to: data/enriched_sales_data.txt")

        # 12. Generate comprehensive report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_transactions,enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # 13. Print success message with file locations
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\nX ERROR OCCURRED")
        print(f"Reason: {e}")
        print("Please check inputs or data files and try again.")


if __name__ == "__main__":
    main()

