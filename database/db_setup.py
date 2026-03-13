import duckdb
import pandas as pd

df = pd.read_csv("datasets/sales_data.csv")

con = duckdb.connect("database/cortex.db")

con.execute("CREATE TABLE sales AS SELECT * FROM df")

print("Database created successfully")