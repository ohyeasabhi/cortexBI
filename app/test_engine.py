from agents.query_agent import generate_sql
from analytics.sql_runner import run_sql

question = input("Ask a question: ")

sql = generate_sql(question)

print("\nGenerated SQL:")
print(sql)

result = run_sql(sql)

print("\nResult:")
print(result)