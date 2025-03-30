import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def generate_graph():
    st.subheader("📊 Dynamic Graph Generator")

    # File Upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Data Preview")
        st.write(df.head())

        # Select X and Y columns
        x_col = st.selectbox("Select X-axis", df.columns)
        y_col = st.selectbox("Select Y-axis", df.columns)

        # Graph Type Selection
        graph_type = st.radio("Select Graph Type", ["Line", "Bar", "Scatter"])

        # Create Graph
        fig = go.Figure()

        if graph_type == "Line":
            fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode="lines", name=y_col))
        elif graph_type == "Bar":
            fig.add_trace(go.Bar(x=df[x_col], y=df[y_col], name=y_col))
        elif graph_type == "Scatter":
            fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode="markers", name=y_col))

        # Customize Layout
        fig.update_layout(
            title=f"{graph_type} Graph of {y_col} vs {x_col}",
            xaxis_title=x_col,
            yaxis_title=y_col,
            plot_bgcolor="rgb(230, 230,230)",
            showlegend=True,
        )

        # Show Graph
        st.plotly_chart(fig)
