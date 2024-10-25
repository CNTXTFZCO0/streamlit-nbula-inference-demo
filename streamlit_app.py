import streamlit as st
from openai import OpenAI

# Initialize session state for API key and base URL
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'base_url' not in st.session_state:
    st.session_state.base_url = ""

st.title("Nbula Interaction")

# Input form for OpenAI API key and base URL
with st.form(key='Nbula Setup'):
    base_url = st.text_input("Enter the NBULA Base URL:", st.session_state.base_url)
    api_key = st.text_input("Enter Your NBULA key:", st.session_state.api_key, type='password')
    save_button = st.form_submit_button(label='Save')

# Save API key and base URL to session state
if save_button:
    st.session_state.api_key = api_key
    st.session_state.base_url = base_url
    st.success("NBULA API Key and Base URL saved!")

# Ensure that the API key and base URL are provided
if st.session_state.api_key and st.session_state.base_url:
    st.subheader("Chat with NBULA Model")

    # Input for message prompt
    message_prompt = st.text_area("Enter your message prompt:", "What is a qbit?")

    if st.button("Send to NBULA"):
        try:
            # Initialize OpenAI client
            client = OpenAI(
                api_key=st.session_state.api_key,
                base_url=st.session_state.base_url,
            )

            # Prepare the chat completion request
            completion = client.chat.completions.create(
                model="meta-llama/Llama-3.2-1B-Instruct",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant, expert in <Quantum Mechanics>. You are trained to <Function>"
                    },
                    {
                        "role": "user",
                        "content": message_prompt
                    }
                ]
            )

            # Display the response from OpenAI
            response_message = completion.choices[0].message.content
            st.success("Response received!")
            st.write(response_message)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.warning("Please provide the OpenAI API key and base URL to proceed.")