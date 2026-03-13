import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px

from agents.query_agent import generate_sql
from agents.insight_agent import generate_insight
from agents.viz_agent import choose_chart

st.set_page_config(page_title="CortexBI", layout="wide")

st.title("🧠 CortexBI — AI Business Intelligence")
st.write("Upload a dataset and chat with your data.")

# -------------------------
# SESSION MEMORY
# -------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------
# DATASET UPLOAD
# -------------------------
uploaded_file = st.file_uploader("Upload CSV dataset", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Create temporary DuckDB table
    con = duckdb.connect()
    con.register("data", df)

    question = st.text_input("Ask a question about the dataset")

    if question:

        columns = ", ".join(df.columns)

        prompt = f"""
Table name: data
Columns: {columns}

Question: {question}
"""

        # Generate SQL with memory
        sql = generate_sql(prompt, st.session_state.chat_history)

        st.subheader("Generated SQL")
        st.code(sql)

        # Execute query
        result = con.execute(sql).fetchdf()

        st.subheader("Query Result")
        st.dataframe(result)

        # -------------------------
        # VISUALIZATION
        # -------------------------
        if len(result.columns) >= 2:

            chart_type = choose_chart(result)

            st.subheader("Visualization")

            fig = None

            if chart_type == "bar":
                fig = px.bar(result, x=result.columns[0], y=result.columns[1])

            elif chart_type == "line":
                fig = px.line(result, x=result.columns[0], y=result.columns[1])

            elif chart_type == "pie":
                fig = px.pie(result, names=result.columns[0], values=result.columns[1])

            if fig:
                st.plotly_chart(fig)

        # -------------------------
        # AI INSIGHT
        # -------------------------
        st.subheader("AI Insight")

        insight = generate_insight(question, result)

        st.write(insight)

        # -------------------------
        # SAVE MEMORY
        # -------------------------
        st.session_state.chat_history.append(
            {
                "question": question,
                "sql": sql
            }
        )

# -------------------------
# SHOW HISTORY
# -------------------------
if st.session_state.chat_history:

    st.subheader("Conversation History")

    for item in st.session_state.chat_history[::-1]:

        st.write("Question:", item["question"])
        st.code(item["sql"])
