
import duckdb

def run_sql(query):

    con = duckdb.connect("database/cortex.db")

    result = con.execute(query).fetchdf()

    return result
