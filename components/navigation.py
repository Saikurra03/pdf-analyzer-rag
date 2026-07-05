import streamlit as st


def show_navigation():
    """Show a simple navigation sidebar with all tools."""
    with st.sidebar:
        st.markdown("## Navigation")
        st.markdown("---")

        # Home button
        if st.button("Home", use_container_width=True, key="nav_home"):
            st.switch_page("Home.py")

        st.markdown("---")
        st.markdown("### Tools")

        # Tool buttons
        tools = [
            ("Chat", "pages/01_chat.py", "💬"),
            ("Summary", "pages/02_summary.py", "📝"),
            ("Notes", "pages/03_notes.py", "📋"),
            ("Flashcards", "pages/04_flashcards.py", "🃏"),
            ("Quiz", "pages/05_quiz.py", "❓"),
            ("Interview", "pages/06_interview.py", "🎤"),
            ("Search", "pages/07_search.py", "🔍"),
            ("Embeddings", "pages/08_embeddings.py", "🧩"),
            ("Vector DB", "pages/09_vector_db.py", "🗄️"),
            ("Analytics", "pages/10_analytics.py", "📊"),
            ("Settings", "pages/11_settings.py", "⚙️"),
            ("RAG Config", "pages/12_rag_config.py", "🔧"),
            ("Current Config", "pages/13_current_config.py", "📋"),
        ]

        for name, path, icon in tools:
            if st.button(f"{icon} {name}", use_container_width=True, key=f"nav_{name}"):
                st.switch_page(path)

        st.markdown("---")
