import sqlite3
import pandas as pd

conn = sqlite3.connect("amazon.db")

query = """
SELECT Category, SUM(Qty) AS total_units_sold
FROM amazon_sales
GROUP BY Category
ORDER BY total_units_sold DESC
LIMIT 10;
"""
result = pd.read_sql_query(query, conn)
print(result)

query2 = """
SELECT Category,
       SUM(Qty * Amount) AS total_revenue
FROM amazon_sales
GROUP BY Category
ORDER BY total_revenue DESC
LIMIT 10;
"""
result2 = pd.read_sql_query(query2, conn)
print(result2)

query3 = """
SELECT `Order ID`, 
       SUM(Qty * Amount) AS total_spent
FROM amazon_sales
GROUP BY `Order ID`
ORDER BY total_spent DESC
LIMIT 10;
"""
result3 = pd.read_sql_query(query3, conn)
print(result3)

query4 = """
SELECT `ship-state`,
       SUM(Qty * Amount) AS total_sales
FROM amazon_sales
GROUP BY `ship-state`
ORDER BY total_sales DESC;
"""
result4 = pd.read_sql_query(query4, conn)
print(result4)

query5 = """
SELECT Status,
       COUNT(*) AS order_count
FROM amazon_sales
GROUP BY Status
ORDER BY order_count DESC;
"""
result5 = pd.read_sql_query(query5, conn)
print(result5)