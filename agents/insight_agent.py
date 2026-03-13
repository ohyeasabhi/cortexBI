import ollama

def generate_insight(question, dataframe):

    sample_data = dataframe.head(20).to_string()

    prompt = f"""
You are a senior business data analyst.

The user asked:
{question}

Query results:
{sample_data}

Write a short business insight explaining the result.
Keep it concise and clear.
"""

    response = ollama.chat(
        model="qwen3-coder:30b",
        messages=[{"role": "user", "content": prompt}]
    )

    insight = response['message']['content']

    return insight
