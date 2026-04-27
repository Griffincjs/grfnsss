import pandas as pd
import sqlite3

# Load CSV file
df = pd.read_csv("amazon_sales.csv")

conn = sqlite3.connect("amazon.db")

df.to_sql("amazon_sales", conn, if_exists="replace", index=False)

print("Data successfully loaded into SQLite database!")