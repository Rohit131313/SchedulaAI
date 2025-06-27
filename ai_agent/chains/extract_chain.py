from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from datetime import datetime
from dotenv import load_dotenv
from typing import Optional
import os

# Load API key
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.environ["GOOGLE_API_KEY"]

# Get current date and day
today = datetime.now()
today_str = today.strftime("%Y-%m-%d")  
day_of_week = today.strftime("%A")      


# Output model
class ExtractAnswer(BaseModel):
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    task: str

# Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=0)
structured_llm = llm.with_structured_output(ExtractAnswer)


template = PromptTemplate(
    input_variables=["user_input", "today_date", "today_day"],
    template="""
You are a scheduling assistant helping to book calendar events.

Today's date is {today_date} and today is {today_day}.

From the user input, extract:
- start_time: ISO 8601 datetime in **UTC (GMT+00)** format (e.g. 2025-06-28T09:30:00Z)
- end_time: ISO 8601 datetime in UTC (assume 1 hour after start if not mentioned)
- task: short summary of the event

Resolve phrases like "tomorrow", "next Thursday", etc. using today’s date and day.

If any value is missing, return `null` (unquoted).

### User input:
"{user_input}"
"""
)


extract_chain = (template| structured_llm)

    

# Run and print output
# response = extract_chain.invoke({"user_input": "Schedule a demo call with client next Thursday at 4 pm",
# "today_date":today_str,"today_day":day_of_week})

# print("Start:", response.start_time)
# print("End:  ", response.end_time)
# print("Task:", response.task)
