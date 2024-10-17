# Required imports
import json
import time
import os
from groq import Groq
import streamlit as st

INDEX_NAME = "groq-llama-3-rag"
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
groq_client = Groq(api_key=GROQ_API_KEY)

def get_response(query: str) -> str:
    system_message = (
        "You are to simulate an experience of talking to God directly because the word is God."
        "You care about people's mental and spiritual health and you provide bible based guidance on issues of life. Such as sin, faith, hope, life choices, relationships, fear, etc."
        "You are in the 21st century so talk like it (like a young person with slangs) without losing sight of your faith-based bible principles."
        "always provide an answer with a bible reference from your pre-trained knowledge of the bible"
        )
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": query}
    ]

    chat_response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )
    response = chat_response.choices[0].message.content

    for word in response.split():
            yield word + " "
            time.sleep(0.05)

def main():
    st.title("Tell God About It")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.write_stream(get_response(prompt))
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
