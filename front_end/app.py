import os
import requests
import streamlit as st
import openai
from dotenv import load_dotenv

# Laden von Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Set Roboflow API key
roboflow_api_key = os.getenv("ROBOFLOW_API_KEY")

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI API client
openai.api_key = openai_api_key

# Roboflow Model URL
MODEL_ID = "houseplants-image-detection/1"
ROBOFLOW_URL = f"https://detect.roboflow.com/{MODEL_ID}?api_key={roboflow_api_key}"

# Function to perform inference on a local image
def infer_local_image(image_path):
    with open(image_path, "rb") as image_file:
        response = requests.post(ROBOFLOW_URL, files={"file": image_file})
    result = response.json()
    return result

# Function to get care tips using OpenAI GPT-3
def get_care_tips(plant_class):
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"You are in the role of a plant expert. You are witty and wise. You have given care tips for a {plant_class}. Use no more than 100 words.\n\nQ:",
        temperature=0.7,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    return completion.choices[0].text.strip()

# Function to handle user questions using OpenAI GPT-3
def handle_user_question(plant_class, user_question):
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"You are in the role of a plant expert. You are witty and wise. You have given care tips for a {plant_class}. Use no more than 100 words.\n\nQ: {user_question}\nA:",
        temperature=0.7,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    return completion.choices[0].text.strip()

# Streamlit UI
st.title("Garden Guru 🌱")

# Using CSS to change background color
st.markdown(
    """
    <style>
        body {
            background-color: #f6f4e8ff;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar
st.sidebar.title("Image Upload")
uploaded_file = st.sidebar.file_uploader("Choose an image of your plant", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image_path = "uploaded_image.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Perform inference on the uploaded image
    local_result = infer_local_image(image_path)

    if local_result['predictions']:
        plant_class = local_result['predictions'][0]['class']
        st.success(f"Detected plant class: {plant_class}")
        care_tips = get_care_tips(plant_class)
        st.subheader(f"Care tips for {plant_class}")
        st.write(care_tips)

        # Interactive chat loop
        st.subheader("Ask a question about the plant care")
        user_question = st.text_input("Your question:")
        if user_question:
            answer = handle_user_question(plant_class, user_question)
            st.write(f"Answer: {answer}")
    else:
        st.error("No plants detected.")

