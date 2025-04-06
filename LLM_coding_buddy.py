import streamlit as st
import numpy as np
import pandas as pd
import datetime
import re

from twython import Twython, TwythonError
import config

from google import genai
from google.genai.types import HttpOptions, ModelContent, Part, UserContent

lang_dict = {'sql': 'sql', 'python':'py'}

st.title('LLM Assistant for Vibe Coding')

st.write('This app allows you to interact with a LLM model (gemini) and assist you through your vibe coding session. This app automatically detects when the model give you a script as a response and you can directly export it as a text file.')

key = Twython(config.api_key)
client = genai.Client(api_key=key)
chat = client.chats.create(model="gemini-2.0-flash", history=[
        UserContent(parts=[Part(text="Hello, I want you to assume a role as a programming mentor that assist a beginner programmer with their coding. Please be concise with your answers.")]),
        ModelContent(
            parts=[Part(text="I a great programmer")],
        ),
    ],
)

# Define session state and create history

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display the chat

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Main code for interaction with the model

prompt = st.chat_input('Say something')

if prompt:

    # The 'user' part which we put an input
    with st.chat_message('user'):
        st.write(prompt)

    st.session_state.messages.append({'role':'user', 'content':prompt}) # add the input into the chat history

    # create response
    response = chat.send_message(prompt)

    # The part where the LLM model responds
    with st.chat_message('assistant'):
        st.write(response.text)
        print(response.text)

    st.session_state.messages.append({'role':'assistant', 'content':response.text})

    # Detect if a script is given in the response using regex

    if '```' in response.text:
        pattern = r"```(?:\w+)?\n(.*?)```"
        matches = re.findall(pattern, response.text, re.DOTALL)
        print(matches)

        lang_patt = '[\n\r]*```[ \t]*([^\n\r]*)'
        lang = re.findall(lang_patt, response.text, re.DOTALL)[0]
        lang_ext = lang_dict.get(str(lang))

        if matches:
            matches = matches[0]
            code_text = "".join(matches)
            print(code_text)

            st.download_button(
                label="Download Extracted Code",
                data=code_text,
                file_name=f"extracted_code_{str(datetime.datetime.now())}.{lang_ext}",
                mime="text/plain"
            )


