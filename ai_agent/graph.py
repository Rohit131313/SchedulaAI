from dotenv import load_dotenv

from langgraph.graph import END, StateGraph

from ai_agent.state import GraphState
from ai_agent.nodes.extract_information import extract_information
from ai_agent.nodes.check_availability import check_and_suggest_around_task
from ai_agent.nodes.settask_in_calendar import settask_in_calendar


load_dotenv()

def route_calendar_flow(state: GraphState):
    print("---ROUTE CALENDER FLOW---")
    if(state['available']):
        return "settask"
    else:
        return "END"

flow = StateGraph(state_schema=GraphState)

flow.add_node("EXTRACTER", extract_information)
flow.add_node("CHECK_AVAILABILITY", check_and_suggest_around_task)
flow.add_node("SETTASK",settask_in_calendar)

flow.set_entry_point("EXTRACTER")

flow.add_edge("EXTRACTER", "CHECK_AVAILABILITY")

flow.add_conditional_edges(
    "CHECK_AVAILABILITY",
    route_calendar_flow,
    path_map={"END": END, "settask": "SETTASK"},
)

flow.add_edge("SETTASK", END)

app = flow.compile()
# app.get_graph().draw_mermaid_png(output_file_path="graph.png")