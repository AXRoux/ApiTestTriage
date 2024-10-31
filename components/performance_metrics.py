import streamlit as st
import plotly.graph_objects as go

def render_performance_metrics(timing):
    """Render performance metrics and visualizations"""
    
    st.subheader("Performance Metrics")
    
    # Create metrics columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Time", f"{timing['total_time']:.3f}s")
    
    with col2:
        st.metric("Response Size", f"{timing['size']/1024:.2f}KB")
    
    with col3:
        st.metric("Status", timing['status_code'])

    # Create timing visualization
    fig = go.Figure(data=[
        go.Bar(
            x=['Response Time'],
            y=[timing['total_time']],
            text=[f"{timing['total_time']:.3f}s"],
            textposition='auto',
        )
    ])

    fig.update_layout(
        title="Response Time",
        yaxis_title="Seconds",
        showlegend=False,
        height=200
    )

    st.plotly_chart(fig, use_container_width=True)
