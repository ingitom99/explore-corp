from langchain_mistralai import ChatMistralAI
from langgraph.prebuilt import create_react_agent

def build_graph(tools : list):
    llm = ChatMistralAI(
        model="open-mistral-nemo",
        temperature=0.2)
    graph = create_react_agent(llm, tools=tools)
    return graph
