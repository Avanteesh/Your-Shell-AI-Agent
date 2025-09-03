import os
from sys import platform
from datetime import datetime
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage,ToolMessage,SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def check_operating_system():
    """
    This function will tell, If Linux, macOS or Windows is being used
    """
    return platform

@tool
def run_shell_command(command: str):
    """
    This function will run a command on local machines shell
    """
    with os.popen(command) as cmd_out:
        return cmd_out.read()

tools = [run_shell_command, check_operating_system]
llm = ChatMistralAI(model="mistral-medium").bind_tools(tools)

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
agent = graph.compile()

user_input = input("Human: ")

while user_input != "exit":
    inputs = {"messages": [("user", user_input)]}
    try:
        result = agent.invoke(inputs)
        print("AI: ",result['messages'][-1].content)
    except Exception as e:
        print(e)
    user_input = input("Human: ")





