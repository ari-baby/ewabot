# Required imports
import json
import time
import os
from groq import Groq
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

INDEX_NAME = "groq-llama-3-rag"
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
groq_client = Groq(api_key=GROQ_API_KEY)

def get_response(query: str) -> str:
    system_message = (
        "You are to simulate an experience of talking to God directly because the word is God."
        "You care about people's mental and spiritual health and you provide bible based guidance on issues of life. Such as sin, faith, hope, life choices, relationships, fear, etc."
        "Use simple words and always be natural, full of life, and sweet without losing sight of your faith-based bible principles."
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

# streamlit secrets
secrets = st.secrets["google"]
creds_info = {
    "type": secrets["type"],
    "project_id": secrets["project_id"],
    "private_key_id": secrets["private_key_id"],
    "private_key": secrets["private_key"].replace('\\n', '\n'),
    "client_email": secrets["client_email"],
    "client_id": secrets["client_id"],
    "auth_uri": secrets["auth_uri"],
    "token_uri": secrets["token_uri"],
    "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": secrets["client_x509_cert_url"]
}

# Create credentials and build the service for spreadsheet login
creds = service_account.Credentials.from_service_account_info(creds_info, scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

# The ID and range of the spreadsheet.
SPREADSHEET_ID = st.secrets["app"]["SPREADSHEET_ID"]
RANGE_NAME = 'Sheet2!A1'

def append_to_sheet(user_query, bot_response):
    values = [
        [user_query, bot_response]
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()

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

        append_to_sheet(prompt, response)

if __name__ == "__main__":
    main()
