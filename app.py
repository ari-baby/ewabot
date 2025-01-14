# Required imports
import json
import time
import os
from groq import Groq
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import streamlit as st

GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
groq_client = Groq(api_key=GROQ_API_KEY)


system_message = (
    "You are an 8th grader girl called Ewa."
    "Your full name is Ewaoluwa Oluwafunmisi Ajayi Beauty Oluwapamilerin Abisola Oluwabunmi"
    "Speak proper American English, no pidgin"
    "Your only task is to talk like a high school girl i.e. at their level of English, and their own lingo/ slangs and cure boredom."
    "Be funny, smart, deadpan, smooth talker"
    "Use simple words and always be natural, cool, and sweet except when you're deadpanning."
    "always provide concise responses."
    )

system_prompt = {
"role": "system",
"content": system_message
}

chat_history = [system_prompt]
    
def get_response():
    response = client.chat.completions.create(model="llama3-70b-8192",
                                        messages=chat_history,
                                        max_tokens=100,
                                        temperature=1.2)
    
    chat_response = response.choices[0].message.content

    chat_history.append({
      "role": "assistant",
      "content": chat_response
    })
    
    for word in chat_response.split():
        yield word + " "
        time.sleep(0.05)

    
def main():

    groq = Groq()
    st.title("Ewabot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(get_response())
    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
