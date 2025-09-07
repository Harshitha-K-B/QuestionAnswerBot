import os
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("💬 Q&A Assistant")

# --- Clear Chat Button ---
if st.button("🧹 Clear Chat"):
    st.session_state["messages"] = []  # Reset chat

# User input
user_input = st.text_input("Type your question:")

if st.button("Send") and user_input:
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state["messages"]
    )
    reply = response.choices[0].message.content

    # Add assistant message
    st.session_state["messages"].append({"role": "assistant", "content": reply})

# --- Display Messages (latest on top) ---
for msg in reversed(st.session_state["messages"]):
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Bot:** {msg['content']}")
