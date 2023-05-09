from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import openai
import os
import uvicorn
from starlette.responses import FileResponse
import json

# Initialize OpenAI API credentials
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Define root endpoint for the chatbot
@app.get("/")
def form():
    return FileResponse('index.html')


# Define endpoint for processing user input and returning chatbot response
@app.post("/chat")
async def chat(query: str = Form(...)):
    # Generate response from OpenAI API
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    print(project_path)
    with open(os.path.join(project_path, "secret.json"), 'r') as jp:
        json_contents = json.loads(jp.read())
    openai.api_key = json_contents['chatgpt_apikey']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[  # Change this
            {"role": "assistant", "content": f"Conversation with the chatbot:\n\nUser: {query}\nBot:"}
        ],
        max_tokens=150,
        n=1,
        temperature=0.5,
    )

    # Extract text from OpenAI API response
    message = response['choices'][0]['message']['content']

    # Return chatbot response
    return HTMLResponse(content=f"<html><body><p>Chatbot: {message}</p></body></html>")


if __name__ =="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
