import streamlit as st
import requests
from PIL import Image

# Defining FastAPI Endpoints
prediction_url = "http://127.0.0.1:8000/prediction"
chat_url = "http://127.0.0.1:8000/chat"

# Setting up the Streamlit Application Title
st.title("Plant Care Predictor and Q&A Chatbot")

# Image upload section
st.header("Upload an Image of Your Plant") # Adds a header for the image upload section
uploaded_file = st.file_uploader("Choose an image...", type="jpg") # Provides a file uploader widget that accepts JPG images

# Handling the Uploaded Image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")

    # Save the uploaded file to a temporary location
    with open("raw_data/temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Send image to FastAPI for prediction
    with open("raw_data/temp_image.jpg", "rb") as f:
        files = {"file": f}
        response = requests.post(prediction_url, files=files)
        care_tips = response.json().get("text", "No care tips available.")

    st.write(f"Care Tips: {care_tips}")

# Chatbot section
st.header("Ask the Plant Care Expert")
plant_class = st.text_input("Enter the plant class (e.g., Begonia rex):")
user_prompt = st.text_input("Enter your question:")

# Handling the User's Question
if st.button("Ask"):        # Adds a button that triggers the chat functionality
    if plant_class and user_prompt:
        params = {"plant_class": plant_class, "user_prompt": user_prompt}
        response = requests.get(chat_url, params=params)
        chat_response = response.json().get("response", "No response available.")
        st.write(f"Expert Answer: {chat_response}")
    else:
        st.write("Please enter both the plant class and your question.")

# Home endpoint response
st.header("Welcome Message")
home_response = requests.get("http://127.0.0.1:8000/")
st.write(home_response.json().get("message", "No welcome message available."))
