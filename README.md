# Sales Analytics System

A complete Python-based **Sales Analytics System** that reads raw sales data, cleans and validates it, performs business analytics, enriches data using an external API, and generates a comprehensive text-based sales report.

---

## Features

-  File handling with multiple encoding support (UTF-8, Latin-1, CP1252)
-  Data parsing, cleaning, and validation
-  User-driven filtering (Region & Amount range)
-  Sales analytics and business insights
-  API integration using DummyJSON
-  Sales data enrichment using API product details
-  Comprehensive text report generation
-  Robust error handling and safe execution

---

## Project Structure

sales-analytics-system/
│
├── data/
│ ├── sales_data.txt
│ └── enriched_sales_data.txt
│
├── output/
│ └── sales_report.txt
│
├── utils/
│ ├── file_handler.py
│ ├── data_processor.py
│ └── api_handler.py
│
├── main.py
├── requirements.txt
└── README.md

---

##  Prerequisites

- Python **3.8+**
- Code editor (VS Code)

---

##  Step And Run Instructions

### 1. Create virtual environment
python -m venv venv

### 2. Activate environment
venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Run the application
python main.py



