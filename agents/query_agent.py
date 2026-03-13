import ollama

def generate_sql(prompt, history=None):

    system_prompt = """
You are a senior data analyst.

IMPORTANT RULES:

1. Use ONLY the columns provided in the schema.
2. Do NOT invent columns.
3. If a column requested by the user does not exist, choose the closest available column.
4. Return ONLY valid SQL.

Example:
If the user asks for category but the table has product,
use product instead.
"""

    messages = [{"role": "system", "content": system_prompt}]

    if history:
        for item in history[-3:]:
            messages.append({"role": "user", "content": item["question"]})
            messages.append({"role": "assistant", "content": item["sql"]})

    messages.append({"role": "user", "content": prompt})

    response = ollama.chat(
        model="qwen3-coder:30b",
        messages=messages
    )

    sql = response['message']['content']

    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql