# Importing Required Libraries
from fastapi import FastAPI, File, UploadFile
from inference_sdk import InferenceHTTPClient
import os
import uvicorn
import openai

from openai import OpenAI
client = OpenAI()

# Set OpenAI API key
openai_api_key = os.environ["OPENAI_API_KEY"]

# Initialize the OpenAI API client
openai.api_key = openai_api_key

os.makedirs("raw_data", exist_ok=True)

# Initializing the FastAPI App
app = FastAPI()

# Initializing the Roboflow API Client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=os.environ["ROBOFLOW_API_KEY"]
)

# Helper functions (placeholders)

# Takes an image path, sends it to the Roboflow API for inference, and returns the detected plant name.
def inference_local_image(image_path: str):
    result = CLIENT.infer(image_path, model_id="houseplants-image-detection/1")
    # Extract plant name from the result (assumption)
    plant_name = result['predictions'][0]['class']
    return plant_name

# Takes a plant name and returns example care tips.
def get_care_tips(plant_name: str):
    # Example care tips based on the plant name (assumption)
    care_tips = f"Care tips for {plant_name}: Water regularly, keep in indirect sunlight."
    return care_tips


# Takes a user prompt and returns an example response.
def handle_user_question(plant_class, user_question):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": f"You are in the role of a plant expert. You are witty and wise. You have given care tips for a {plant_class}. Use no more than 100 words."},
            {"role": "user", "content": f"{user_question}"}
        ]
    )
    return completion.choices[0].message.content

# API Endpoints 
@app.post("/prediction")  # Method: POST
async def prediction(file: UploadFile = File(...)):
    file_location = f"raw_data/_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    plant = inference_local_image(file_location)
    care_tips = get_care_tips(plant)
    return {"text": care_tips}  # Returns the care tips as a JSON response.

# chat Endpoint
@app.get("/chat")  # Method: GET
async def chat(plant_class: str, user_prompt: str):
    response = handle_user_question(plant_class, user_prompt)
    return {"response": response} # Returns the response as a JSON response.

@app.get("/")
def home():
    return {"message": "Welcome to the chatbot API!"}
# Running the Application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


# The script sets up a FastAPI application with two endpoints: one for predicting plant care tips from an uploaded image and another for a simple Q&A chatbot.