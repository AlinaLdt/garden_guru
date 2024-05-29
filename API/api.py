from fastapi import FastAPI

app = FastAPI()

@app.get('/prediction')

def prediction(image):
  plant = inference_local_image(image)
  care_tips = get_care_tips(plant)
  return ["text":care_tips]

@app.get('/chat')

def chat (user_prompt):
  = handle_user_question(user_prompt)

unicorn api:app --reload
