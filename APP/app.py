import streamlit as st
import requests
from PIL import Image
import io

# FastAPI server URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Function to make predictions
def get_prediction(image_data):
    files = {"image": image_data}
    response = requests.post(f"{FASTAPI_URL}/prediction", files=files)
    return response.json()

# Function to handle chat
def get_chat_response(user_prompt):
    data = {"user_prompt": user_prompt}
    response = requests.post(f"{FASTAPI_URL}/chat", json=data)
    return response.json()

# Streamlit app
st.title("Garden Guru")

# Image upload
st.header("Upload an image of a plant or mushroom")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()

    # Get prediction
    st.write("Classifying...")
    result = get_prediction(image_bytes)
    st.write(result)

# Chat interface
st.header("Ask a question about your plant or mushroom")
user_prompt = st.text_input("Enter your question:")
if st.button("Ask"):
    if user_prompt:
        chat_response = get_chat_response(user_prompt)
        st.write(chat_response["response"])
    else:
        st.write("Please enter a question.")
