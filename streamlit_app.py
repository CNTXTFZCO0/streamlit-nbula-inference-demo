import streamlit as st
from openai import OpenAI
import time

# Initialize session state for API key, base URL, and model
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'base_url' not in st.session_state:
    st.session_state.base_url = ""
if 'model' not in st.session_state:
    st.session_state.model = ""

st.title("Nbula Interaction")

# Input form for OpenAI API key, base URL, and model
with st.form(key='Nbula Setup'):
    base_url = st.text_input("Enter the NBULA Base URL:", st.session_state.base_url)
    api_key = st.text_input("Enter Your NBULA Key:", st.session_state.api_key, type='password')
    model = st.text_input("Enter Model Name:", st.session_state.model)
    save_button = st.form_submit_button(label='Save')

# Save API key, base URL, and model to session state
if save_button:
    st.session_state.api_key = api_key
    st.session_state.base_url = base_url
    st.session_state.model = model
    st.success("NBULA API Key, Base URL, and Model saved!")

# Ensure that the API key, base URL, and model are provided
if st.session_state.api_key and st.session_state.base_url and st.session_state.model:
    st.subheader("Chat with NBULA Model")

    # Input for message prompt
    message_prompt = st.text_area("Enter your message prompt:", "What is the best time to visit Dubai?")

    if st.button("Send to NBULA"):
        try:
            # Initialize OpenAI client
            client = OpenAI(
                api_key=st.session_state.api_key,
                base_url=st.session_state.base_url,
            )
            start_time = time.time()

            # Prepare the chat completion request
            completion = client.chat.completions.create(
                model=st.session_state.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. You are trained to help with user query"
                    },
                    {
                        "role": "user",
                        "content": message_prompt
                    }
                ]
            )

            end_time = time.time()
            response_time = end_time - start_time

            # Display the response from OpenAI
            response_message = completion.choices[0].message.content
            st.success("Response received!")
            st.write(response_message)
            st.info(f"Inference time: {response_time:.2f} seconds")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.warning("Please provide the Nbula API key, base URL, and model to proceed.")
