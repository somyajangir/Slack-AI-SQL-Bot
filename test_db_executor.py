# test_db_executor.py
"""
Test database executor with pooling
"""

from db import db_executor

# Test queries
test_queries = [
    ("All records", "SELECT * FROM sales_daily LIMIT 5"),
    (
        "Revenue by region",
        "SELECT region, SUM(revenue) as total FROM sales_daily GROUP BY region"
    ),
    (
        "Total records",
        "SELECT COUNT(*) as total_records FROM sales_daily"
    ),
]

print("Testing database executor...")
print("=" * 70)

for name, sql in test_queries:
    print(f"\nTest: {name}")
    print(f"SQL: {sql}")
    print("-" * 70)

    try:
        columns, rows, info = db_executor.execute_query(sql)

        print(f"Columns: {columns}")
        print(f"Rows: {rows}")
        print(f"Info: {info}")

    except Exception as e:
        print(f"Error: {e}")

print("\n" + "=" * 70)
print("Testing complete!")

# Close pool after testing
db_executor.close()