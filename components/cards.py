import streamlit as st
def metric_card(title, value, icon="", color="#1E88E5"):
    """Single metric card."""
    html = f"""
    <div style="
        background: linear-gradient(135deg, {color}11, {color}05);
        border-left: 4px solid {color};
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 12px;
    ">
        <div style="font-size: 13px; color: #888; text-transform: uppercase; letter-spacing: 1px;">
            {icon} {title}
        </div>
        <div style="font-size: 28px; font-weight: 700; color: {color}; margin-top: 6px;">
            {value}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
def info_card(title, content, icon="ℹ️"):
    """Expandable info card."""
    with st.container():
        st.markdown(f"**{icon} {title}**")
        st.markdown(content)
        st.divider()
def status_card(status, message=""):
    """Shows success/error/warning card."""
    colors = {
        "success": ("#43A047", "✅"),
        "error": ("#E53935", "❌"),
        "warning": ("#FB8C00", "⚠️"),
        "info": ("#1E88E5", "ℹ️"),
    }
    color, icon = colors.get(status, colors["info"])
    html = f"""
    <div style="
        background: {color}11;
        border: 1px solid {color}33;
        border-radius: 8px;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    ">
        <span style="font-size: 20px;">{icon}</span>
        <span style="color: {color}; font-weight: 500;">{message or status.title()}</span>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
