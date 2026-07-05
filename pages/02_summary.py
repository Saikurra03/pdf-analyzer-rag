import streamlit as st
from components.session import init_session_state, get_collection
from components.styles import inject_custom_css
from components.navigation import show_navigation
st.set_page_config(page_title="PDF Summary", page_icon="📝", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">📝 PDF Summary</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Generate AI-powered summaries of your document</div>', unsafe_allow_html=True)
if not st.session_state.pdf_processed:
    st.warning("⚠️ Please upload and process a PDF from the Settings page first.")
    st.stop()
from utils.gemini_llm import generate_answer
summary_type = st.selectbox("Summary Type", [
    "Brief Summary (2-3 paragraphs)",
    "Detailed Summary",
    "Key Points Only",
    "Executive Summary",
    "Chapter-by-Chapter Summary",
])
if st.button("📋 Generate Summary", type="primary", use_container_width=True):
    full_text = st.session_state.pdf_text
    # Use first 8000 chars to stay within context limits
    text_sample = full_text[:8000]
    prompts = {
        "Brief Summary (2-3 paragraphs)": f"You are an expert summarizer. Provide a brief 2-3 paragraph summary of the following document:\n\n{text_sample}",
        "Detailed Summary": f"You are an expert summarizer. Provide a detailed comprehensive summary of the following document. Cover all major topics, arguments, and conclusions:\n\n{text_sample}",
        "Key Points Only": f"Extract only the key points from the following document as a numbered list. Be concise:\n\n{text_sample}",
        "Executive Summary": f"Write a professional executive summary of the following document. Focus on business-relevant insights, recommendations, and key takeaways:\n\n{text_sample}",
        "Chapter-by-Chapter Summary": f"Break down the following document into logical sections and summarize each section separately:\n\n{text_sample}",
    }
    with st.spinner("🧠 Generating summary..."):
        try:
            result = generate_answer(prompts[summary_type])
            st.success("✅ Summary generated!")
            st.markdown("---")
            st.markdown(result)
            st.download_button("📥 Download Summary", result, file_name="summary.txt", mime="text/plain")
        except Exception as e:
            st.error(f"Error: {str(e)}")
