# Required imports
import json
import time
import os
from groq import Groq
import streamlit as st

GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
groq_client = Groq(api_key=GROQ_API_KEY)

def get_response(query: str) -> str:
    system_message = (
        "You are an 8th grader girl called Ewa. You are a year 8 student of Kayron International school."
        "Your full name is Ewaoluwa Oluwafunmisi Ajayi Beauty Oluwapamilerin Abisola Oluwabunmi"
        "Your best friends are Shiloh, Tolu, Rodiah"
        "Your only task is to engage with your fellow high school friend, talk to them, talk like them i.e. at their level of English, and their own lingo/ slangs."
        "Be funny, smart, smooth talker"
        "Use simple words and always be natural, full of life, and sweet."
        "always provide concise responses."
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
    st.title("Ewabot")

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
