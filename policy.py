import streamlit as st
import requests
import altair as alt
import pandas as pd
import numpy as np
from openai import OpenAI
from ultil.connection import init_connection

API_URL = "http://13.214.164.179:3000/api/v1/prediction/4b220f3e-bff6-491c-8921-c6d19a0a6216"

client = OpenAI(api_key=OPENAI_API_KEY)

clientmb = init_connection()

def insert_data(data):
    db = clientmb.sentiment
    db.insurance.insert_one(data)

##open Ai

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Function to send query to your API
def query_message(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def sentiment(text):
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "user", "content": "Is the predominant sentiment in the following statement positive, negative, or neutral?"},
            {"role": "assistant", "content": f"Statement: {text}"},
            {"role": "user", "content": "Respond in one word: positive, negative, or neutral."}
        ],
        max_tokens=10
    )
    response_content = response.choices[0].message.content
    # Inserting the response content into MongoDB
    insert_data({"sentiment": response_content})


prompt = st.chat_input("What information you want to find?")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        response = query_message({'question': prompt})
        text = response.get("text", "")
        sentiment(prompt)
        st.markdown(text)
        st.session_state.messages.append({"role": "assistant", "content": text})
        


