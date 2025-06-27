from typing import Any, Dict

from ai_agent.state import GraphState
from ai_agent.chains.extract_chain import extract_chain
from datetime import datetime

# Get current date and day
today = datetime.now()
today_str = today.strftime("%Y-%m-%d")  
day_of_week = today.strftime("%A")      


def extract_information(state: GraphState) -> Dict[str, Any]:
    """
    Extract date , time and task to schedule.

    Args:
        state (dict): The current state of the graph.

    Returns:
        state (dict): A dictionary containing the date, time, task.
    """
    print("---EXTRACTING INFORMATION---")
    input = state['input']
    generation = extract_chain.invoke({
        "user_input":input,
        "today_date":today_str,
        "today_day":day_of_week
        })
    print(f"start_time : {generation.start_time} , end_time: {generation.end_time}, task : {generation.task}")
    return {
        "start_time":generation.start_time, 
        "end_time": generation.end_time, 
        "task": generation.task
        }