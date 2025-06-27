from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_runner import run_agent

app = FastAPI()

# CORS setup (for Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputModel(BaseModel):
    input: str

@app.post("/process/")
async def process_input(data: InputModel):
    result = run_agent(data.input)
    return result
