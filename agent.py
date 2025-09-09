import os
from json import dumps
from requests import get
from sys import platform
from datetime import datetime, timedelta
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage,ToolMessage,SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from random import choice
from base64 import b64encode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def check_operating_system() -> str:
    """
    This function will tell, If Linux, macOS or Windows is being used
    """
    return platform

@tool
def run_shell_command(command: str) -> str:
    """
    This function will run a command on local machines shell
    """
    with os.popen(command) as cmd_out:
        return cmd_out.read()

@tool
def tell_weather(location: str) -> str:
    """
    This function will tell, whats the weather, current time and its latitude longitude
    in a specific location!
    """
    api_key = os.getenv("WEATHER_API_KEY")
    fetch_data = get(f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no")
    if not fetch_data.ok:
        return f"{'{'}\"message\": \"Could not get weather data of {location}\"{'}'}"
    json_res = fetch_data.json()
    return dumps(json_res)

@tool
def get_latest_news(topic: str) -> str:
    """
    This function will tell, whats the latest news headline on a specific Topic!
    """
    api_key = os.getenv("NEWS_API_KEY")
    now = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    fetch_data = get(f"https://newsapi.org/v2/everything?q={topic}&from={now}&sortBy=publishedAt&apiKey={api_key}")
    if not fetch_data.ok:
        return "{\"status\": \"failed\"}"
    json_res = fetch_data.json()
    if len(json_res["articles"]) == 0:
        return "{\"message\": \"No latest headlines found!\"}"
    choice_article = choice(json_res["articles"])
    return dumps(choice_article)

@tool
def get_planetary_positions(lat: int=10.00, long: int=10.00) -> str:
    """
    This function will tell, where the moon, sun and planets are in the sky right now!
    """
    astro_app_key = os.getenv("ASTRO_AUTH_STRING")
    authheader = {
     "Authorization": f"Basic {b64encode(astro_app_key.encode()).decode()}"
    }
    astro_url = "https://api.astronomyapi.com/api/v2/bodies/positions"
    curr_time = datetime.now()
    param_dict = {
     "longitude": 10.00,"latitude": 10.00,"elevation": 1,
     "from_date": curr_time.strftime("%Y-%m-%d"),
     "to_date": curr_time.strftime("%Y-%m-%d"),
     "time": curr_time.strftime("%H:%M:%S")
    }
    response = get(astro_url, headers=authheader, params=param_dict)
    if not response.ok:
        return "Failed to get data"
    json_res = response.json()
    return dumps(json_res["data"]["table"]["rows"])


tools = [
  run_shell_command, check_operating_system, 
  tell_weather,get_latest_news, 
  get_planetary_positions
]
llm = ChatGroq(model="llama-3.1-8b-instant").bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    sys_prompt = SystemMessage(
     content="Your are my AI assistant, Please answer my query at best of your ability."
    )
    response = llm.invoke([sys_prompt] + state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState):
    message = state["messages"]
    last_message = message[-1]
    if not last_message.tool_calls:
        return "end"
    return "continue"

tool_node = ToolNode(tools=tools)
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)
graph.add_node("tools", tool_node)
graph.set_entry_point("our_agent")
graph.add_conditional_edges(
  "our_agent",should_continue,
  {"continue":"tools","end":END}
)
graph.add_edge("tools", "our_agent")
ShellAgent = graph.compile()


