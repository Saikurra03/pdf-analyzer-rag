import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
def similarity_gauge(score):
    """Gauge chart for similarity score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(score, 4),
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Similarity Score", "font": {"size": 14}},
        gauge={
            "axis": {"range": [0, 1], "tickwidth": 1},
            "bar": {"color": "#1E88E5"},
            "steps": [
                {"range": [0, 0.3], "color": "#E5393522"},
                {"range": [0.3, 0.6], "color": "#FB8C0022"},
                {"range": [0.6, 1], "color": "#43A04722"},
            ],
            "threshold": {
                "line": {"color": "#1E88E5", "width": 3},
                "thickness": 0.8,
                "value": score,
            },
        },
    ))
    fig.update_layout(height=250, margin=dict(t=60, b=20, l=40, r=40))
    st.plotly_chart(fig, use_container_width=True)
def chunk_distribution_chart(chunks):
    """Bar chart of chunk lengths."""
    lengths = [len(c) for c in chunks]
    fig = px.bar(
        x=list(range(1, len(lengths) + 1)),
        y=lengths,
        labels={"x": "Chunk Number", "y": "Character Count"},
        title="Chunk Size Distribution",
        color_discrete_sequence=["#1E88E5"],
    )
    fig.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)
def embedding_scatter(embeddings_2d, labels=None):
    """2D scatter plot of embeddings (requires dimensionality reduction upstream)."""
    fig = px.scatter(
        x=embeddings_2d[:, 0],
        y=embeddings_2d[:, 1],
        color=labels,
        title="Embedding Space Visualization",
        labels={"x": "Dimension 1", "y": "Dimension 2"},
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
def distance_bar_chart(distances):
    """Horizontal bar chart of retrieval distances."""
    similarities = [1 - d for d in distances]
    labels = [f"Chunk {i+1}" for i in range(len(distances))]
    colors = ["#43A047" if s > 0.6 else "#FB8C00" if s > 0.3 else "#E53935" for s in similarities]
    fig = go.Figure(go.Bar(
        y=labels,
        x=similarities,
        orientation="h",
        marker_color=colors,
        text=[round(s, 4) for s in similarities],
        textposition="auto",
    ))
    fig.update_layout(
        title="Retrieval Similarity Scores",
        xaxis_title="Similarity",
        yaxis_title="",
        height=200,
        margin=dict(l=80),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
