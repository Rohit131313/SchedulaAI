from ai_agent.graph import app 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.environ["GOOGLE_API_KEY"]

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=0)

# Final user-facing message prompt
final_output_prompt = PromptTemplate(
    input_variables=[
        "task", "start_time", "end_time", "available", "event_link", "suggestions"
    ],
    template="""
You are a helpful assistant generating a final message to the user after checking their calendar.

Here is the task: "{task}"
Start time: {start_time}
End time: {end_time}
Was the requested slot available? {available}

If available:
- Provide a confirmation message that the event has been scheduled.
- Include the event link: {event_link}

If not available:
- Apologize that the slot is already booked.
- Suggest these available alternative time slots in a user-friendly way:
{suggestions}

Your response should be clear, friendly, and concise.
"""
)

chain = final_output_prompt | llm


def run_agent(user_input: str) -> dict:
    output = app.invoke(input={"input": user_input})
    
    if not output.get("event_link"):
        output['event_link'] = "No event was scheduled."


    final_output_prompt = PromptTemplate(
        input_variables=[
            "task", "start_time", "end_time", "available", "event_link", "suggestions"
        ],
        template="""
        You are a helpful assistant generating a final message to the user after checking their calendar.

        Here is the task: "{task}"
        Start time: {start_time}
        End time: {end_time}
        Was the requested slot available? {available}

        If available:
        - Provide a confirmation message that the event has been scheduled.
        - Include the event link: {event_link}

        If not available:
        - Apologize that the slot is already booked.
        - Suggest these available alternative time slots in a user-friendly way:
        {suggestions}

        Your response should be clear, friendly, and concise.
        """
    )

    chain = (final_output_prompt| llm)
    
    response = chain.invoke({
        "task": output['task'],
        "start_time": output['start_time'],
        "end_time": output['end_time'],
        "available": output['available'],
        "event_link": output['event_link'],
        "suggestions": output['suggestions']
    })

    output = response.content
    return output

# print(run_agent("Schedule a call with Rohit next Thursday from at 4 pm"))
