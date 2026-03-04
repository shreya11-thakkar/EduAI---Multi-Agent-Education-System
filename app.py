# app.py
import streamlit as st
from multi_agent import run_education_system
from database import get_all_topics, get_note, create_table
create_table() 

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(
    page_title="EduAI - Multi Agent Learning System",
    page_icon="🎓",
    layout="wide"
)

# ------------------ SIDEBAR ------------------ #
with st.sidebar:
    st.title("🎓 EduAI")
    st.markdown("### Multi-Agent Education System")
    st.markdown("---")

    difficulty = st.selectbox(
        "Select Difficulty Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    st.markdown("---")
    st.markdown("### 📚 Saved History")

    topics = get_all_topics()

    if topics:
        selected_topic = st.selectbox("Select a topic", topics)

        if st.button("Load Topic"):
            note = get_note(selected_topic)

            # Reset chat
            st.session_state.messages = []

            st.session_state.messages.append({
                "role": "user",
                "content": selected_topic
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": note
            })
    else:
        st.caption("No saved topics yet")

# ------------------ HEADER ------------------ #
st.title("🎓 EduAI Learning Assistant")
st.markdown("Your AI Researcher + AI Writer working together to generate structured study notes.")
st.markdown("---")

# ------------------ SESSION STATE ------------------ #
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ DISPLAY CHAT (IMPORTANT) ------------------ #
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ USER INPUT ------------------ #
user_input = st.chat_input("Enter your study topic here...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        with st.spinner("EduAI Agents are researching and writing..."):
            topic_with_level = f"{user_input} (Difficulty: {difficulty})"
            result = run_education_system(topic_with_level)
            st.markdown(result)

    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })

# ------------------ FOOTER ------------------ #
st.markdown("---")
st.caption("© 2026 EduAI | Multi-Agent Education System")
