import streamlit as st
from components.session import init_session_state
from components.styles import inject_custom_css
from components.navigation import show_navigation
st.set_page_config(page_title="Quiz", page_icon="❓", layout="wide")
inject_custom_css()
init_session_state()
show_navigation()
st.markdown('<div class="page-title">❓ Quiz</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Test your knowledge from the PDF</div>', unsafe_allow_html=True)
if not st.session_state.pdf_processed:
    st.warning("⚠️ Please upload and process a PDF from the Settings page first.")
    st.stop()
from utils.gemini_llm import generate_answer
import json
tab_gen, tab_take = st.tabs(["🤖 Generate Quiz", "📝 Take Quiz"])
with tab_gen:
    num_q = st.slider("Number of questions", 3, 15, 5)
    q_type = st.selectbox("Question Type", ["Multiple Choice", "True/False", "Short Answer"])
    if st.button("❓ Generate Quiz", type="primary", use_container_width=True):
        text = st.session_state.pdf_text[:6000]
        fmt = "multiple_choice" if q_type == "Multiple Choice" else "true_false" if q_type == "True/False" else "short_answer"
        prompt = f"""Create {num_q} {q_type} quiz questions from this document.
Return ONLY valid JSON array (no markdown, no code blocks):
[{{"question": "...", "options": ["A","B","C","D"], "answer": "A", "explanation": "..."}}]
For True/False use options: ["True", "False"]
For Short Answer use options: [] and answer as text.
Document:
{text}"""
        with st.spinner("🧠 Generating quiz..."):
            try:
                raw = generate_answer(prompt)
                cleaned = raw.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
                    cleaned = cleaned.rsplit("```", 1)[0]
                questions = json.loads(cleaned)
                st.session_state.quiz_questions = questions
                st.success(f"✅ Generated {len(questions)} questions!")
            except Exception as e:
                st.error(f"Failed to parse: {e}\n\nRaw:\n{raw}")
with tab_take:
    if not st.session_state.quiz_questions:
        st.info("📭 No quiz generated yet.")
    else:
        score = 0
        answers = {}
        for i, q in enumerate(st.session_state.quiz_questions):
            st.markdown(f"**Q{i+1}.** {q['question']}")
            if q.get("options"):
                ans = st.radio(f"Select answer", q["options"], key=f"q_{i}", index=None)
                answers[i] = ans
            else:
                answers[i] = st.text_input("Your answer", key=f"q_{i}_text")
            st.divider()
        if st.button("📊 Submit Quiz", type="primary"):
            for i, q in enumerate(st.session_state.quiz_questions):
                correct = q["answer"]
                user_ans = answers.get(i, "")
                if str(user_ans).strip().lower() == str(correct).strip().lower():
                    score += 1
            st.success(f"🎉 Score: {score}/{len(st.session_state.quiz_questions)}")
            for i, q in enumerate(st.session_state.quiz_questions):
                st.markdown(f"**Q{i+1}:** {q['question']}")
                st.markdown(f"✅ Correct: `{q['answer']}` | Your answer: `{answers.get(i, 'N/A')}`")
                if q.get("explanation"):
                    st.markdown(f"💡 {q['explanation']}")
                st.divider()
