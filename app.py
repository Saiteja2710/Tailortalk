import streamlit as st
import requests
import base64

st.title("Titanic Chatbot 🚢")

user_input = st.text_input("Ask a question about Titanic passengers:")

if st.button("Ask"):  
    response = requests.post("http://127.0.0.1:8000/query", json={"question": user_input})
    data = response.json()
    
    st.write(data["answer"])
    
    if "image" in data:
        img_data = base64.b64decode(data["image"])
        st.image(img_data, caption="Visualization", use_column_width=True)

st.write("\n*Note: Ensure titanic.csv is in the same directory as the backend*")
