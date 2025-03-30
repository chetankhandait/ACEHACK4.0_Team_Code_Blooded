import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List
from phi.assistant import Assistant
from phi.utils.log import logger
from assistant import get_sql_assistant
import sqlite3
import re

def generate_graph():
    st.subheader("\U0001F4CA Dynamic Graph Generator")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Data Preview")
        st.write(df.head())

        x_col = st.selectbox("Select X-axis", df.columns)
        y_col = st.selectbox("Select Y-axis", df.columns)

        graph_type = st.radio("Select Graph Type", ["Line", "Bar", "Scatter"])

        fig = go.Figure()

        if graph_type == "Line":
            fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode="lines", name=y_col))
        elif graph_type == "Bar":
            fig.add_trace(go.Bar(x=df[x_col], y=df[y_col], name=y_col))
        elif graph_type == "Scatter":
            fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode="markers", name=y_col))

        fig.update_layout(
            title=f"{graph_type} Graph of {y_col} vs {x_col}",
            xaxis_title=x_col,
            yaxis_title=y_col,
            plot_bgcolor="rgb(230, 230,230)",
            showlegend=True,
        )

        st.plotly_chart(fig)

st.set_page_config(
    page_title="SQL Assistant",
    page_icon=":orange_heart:",
    layout="wide",
)

st.title("SQL Assistant")
st.markdown("##### :orange_heart")

col1, col2 = st.columns([2, 1])

with col1:
    with st.expander(":rainbow[:point_down: Example Questions]"):
        st.markdown("- Which driver has the most race wins?")
        st.markdown("- Which team won the most Constructors Championships?")

class SQLQuery:
    def __init__(self, query: str):
        self.query = query

def check_sql_syntax(query: str) -> str:
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute(f"EXPLAIN QUERY PLAN {query}")
        conn.close()
        return "Valid SQL Syntax"
    except Exception as e:
        return f"Invalid SQL Syntax: {str(e)}"

def extract_sql(query: str) -> str:
    sql_pattern = re.compile(r'CREATE TABLE|SELECT|INSERT INTO|UPDATE|DELETE FROM', re.IGNORECASE)
    if sql_pattern.search(query):
        return query
    return ""

def main() -> None:
    sql_assistant: Assistant
    if "sql_assistant" not in st.session_state or st.session_state["sql_assistant"] is None:
        sql_assistant = get_sql_assistant()
        st.session_state["sql_assistant"] = sql_assistant
    else:
        sql_assistant = st.session_state["sql_assistant"]

    st.session_state["sql_assistant_run_id"] = sql_assistant.create_run()
    assistant_chat_history = sql_assistant.memory.get_chat_history()
    if len(assistant_chat_history) > 0:
        st.session_state["messages"] = assistant_chat_history
    else:
        st.session_state["messages"] = [{"role": "assistant", "content": "Ask me about F1 data from 1950 to 2020."}]

    with col1:
        if prompt := st.chat_input():
            st.session_state["messages"].append({"role": "user", "content": prompt})
            sql_check_result = check_sql_syntax(prompt)
            st.sidebar.write(f"SQL Check: {sql_check_result}")

        for message in st.session_state["messages"]:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                st.write(message["content"])

        last_message = st.session_state["messages"][-1]
        if last_message.get("role") == "user":
            question = last_message["content"]
            with st.chat_message("assistant"):
                with st.spinner("Working..."):
                    response = ""
                    resp_container = st.empty()
                    for delta in sql_assistant.run(question):
                        response += delta
                        resp_container.markdown(response)
                    st.session_state["messages"].append({"role": "assistant", "content": response})
                    extracted_sql = extract_sql(response)
                    if extracted_sql:
                        sql_check_result = check_sql_syntax(extracted_sql)
                        st.sidebar.write(f"AI SQL Check: {sql_check_result}")

    with col2:
        generate_graph()
        st.subheader("SQL Query Compiler")
        sql_query = st.text_area("Write your SQL query here:")
        if st.button("Check Syntax"):
            syntax_result = check_sql_syntax(sql_query)
            st.code(syntax_result, language="sql")

    st.sidebar.markdown("---")
    if st.sidebar.button("New Run"):
        restart_assistant()
    # if st.sidebar.button("Auto Rename Thread"):
        # sql_assistant.auto_rename_run()
    
    sql_assistant_run_name = sql_assistant.run_name
    if sql_assistant_run_name:
        st.sidebar.write(f":thread: {sql_assistant_run_name}")

def restart_assistant():
    st.session_state["sql_assistant"] = None
    st.session_state["sql_assistant_run_id"] = None
    st.rerun()

if __name__ == "__main__":
    main()
