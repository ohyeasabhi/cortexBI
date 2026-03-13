import ollama

def generate_sql(prompt, history=None):

    system_prompt = """
You are a senior data analyst.

Convert the user question into SQL.

Use previous conversation context if helpful.

Return ONLY SQL.
"""

    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation memory
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

    # Clean formatting
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql
