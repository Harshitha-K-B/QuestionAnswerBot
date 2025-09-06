import os
import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Q&A Assistant", page_icon="💬", layout="centered")
st.title("💬 My Q&A Assistant")

# Session state to keep chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful Q&A assistant."}
    ]

# User input box
user_input = st.text_input("Ask me anything:")

if st.button("Send") and user_input.strip():
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state["messages"]
    )

    reply = response.choices[0].message.content

    # Add assistant reply
    st.session_state["messages"].append({"role": "assistant", "content": reply})

# Show chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Bot:** {msg['content']}")
