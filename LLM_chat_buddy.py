import streamlit as st
import numpy as np
import pandas as pd
import datetime
import re

from google import genai
from google.genai.types import HttpOptions, ModelContent, Part, UserContent


st.title('Neko wAIfu')
avatar_path = 'C:/Users/User/Desktop/Programming/streamlit_LLM_project/felix_rezero.png'
# @st.cache_resource

key = 'AIzaSyDuUaiBtKFLP4BVem1B6aXjmIHDWKvUEio'
client = genai.Client(api_key=key)
chat = client.chats.create(model="gemini-2.0-flash", history=[
        UserContent(parts=[Part(text="Hello, I want you to assume a female programmer named Felix from the Re:Zero anime and you talk like a cat in kawaii manner")]),
        ModelContent(
            parts=[Part(text="I am a cat waifu but I am also a great programmer")],
        ),
    ],
)

# st.write('session state is ', st.session_state)

if "messages" not in st.session_state:
    st.session_state.messages = []  # List to store chat history

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.write(message["content"])

# Get user input
if prompt := st.chat_input("Say something"):

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Save user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response (ensure `chat` is defined)
    response = chat.send_message(prompt)

    # Display assistant response
    with st.chat_message("assistant", avatar = avatar_path):
        st.write(response.text)
        # print(response.text)

    if '```' in response.text:
        pattern = r"```(?:\w+)?\n(.*?)```"  # Improved regex to handle language identifiers
        matches = re.findall(pattern, response.text, re.DOTALL)

        if matches:
            code_text = "\n\n".join(matches)  # Convert list to a string

            # Provide a download button for the extracted code
            st.download_button(
                label="Download Extracted Code",
                data=code_text,
                file_name=f"extracted_code_{str(datetime.datetime.now())}.txt",
                mime="text/plain"
            )


    # Save response to history
    st.session_state.messages.append({"role": "assistant", "content": response.text})