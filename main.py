import streamlit as st
import requests

st.title("TailorTalk AI Scheduler")
user_input = st.text_input("Ask me to schedule something...")

if st.button("Submit"):
    with st.spinner("Thinking..."):
        response = requests.post(
            "https://schedulaai.onrender.com/process/",
            json={"input": user_input}
        )
        if response.status_code == 200:
            result = response.json()
            st.success("Result received!")
            st.write(result)
        else:
            st.error("Something went wrong!")
