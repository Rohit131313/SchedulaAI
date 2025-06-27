from typing import TypedDict,List,Dict, Annotated, Optional
from datetime import datetime

class GraphState(TypedDict, total=False):
    """
    Represents the state of a scheduling graph, holding information about
    the desired date, time, and task to be scheduled.
    """
    start_time: datetime
    end_time: datetime
    task: Annotated[str, "Task to schedule"]
    input: Annotated[str, "Input by user"]
    available: bool
    suggestions: List[Dict[str, str]]
    event_link: str

