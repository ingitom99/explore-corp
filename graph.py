import os
import json

import streamlit as st

from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_mistralai import MistralAIEmbeddings

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.tools.retriever import create_retriever_tool

from tools.fzul_tools import fzul_tools_list
from tools.web_tool import web_search_tool
from tools.semanticscholar_tool import academic_search_tool
from tools.epo_tool import patent_search_tool
from tools.rd_tool import rd_info_tool
from tools.sota_tool import combined_search_tool


load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")

custom_tools = [
    web_search_tool,
    combined_search_tool,
    patent_search_tool,
    rd_info_tool,
    academic_search_tool
    ] + fzul_tools_list

llm = ChatMistralAI(
    model="mistral-large-latest",
    api_key=mistral_api_key,
    temperature=0.5
    )

llm_with_tools = llm.bind_tools(custom_tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def agent(state: State):
    system_message = SystemMessage(content="""
    """)
    response = llm_with_tools.invoke([system_message] + state["messages"])
    return {"messages": state["messages"] + [("assistant", response.content)]}

# Graph setup
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("agent", agent)
graph_builder.add_node("tools", ToolNode(tools=custom_tools))

# Add edges
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges(
    "agent",
    tools_condition
)
graph_builder.add_edge("tools", "agent")

# Compile the graph
graph = graph_builder.compile()

def get_response(user_query, chat_history):
    # Prepare the state for the graph
    state = {
        "messages": [
            {"role": "human", "content": msg.content} if isinstance(msg, HumanMessage) else {"role": "assistant", "content": msg.content}
            for msg in chat_history
        ]
    }
    state["messages"].append({"role": "human", "content": user_query})

    # Invoke the graph
    response = graph.invoke(state)
    assistant_message = response["messages"][-1].content
    return assistant_message

# app config
st.set_page_config(
    page_title="IBO",
    page_icon="./ib_logo.svg",
    layout="centered"
)

# Create a layout with two columns
col1, col2 = st.columns([3, 1])

with col1:
    st.title(":gray[Talk to IBO!]")

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hi, I'm IBO..."),
    ]

# Add this button before the chat history display
with st.sidebar:
    if st.button("Refresh chat..."):
        st.session_state.chat_history = [
            AIMessage(content="Hello, I'm IBO"),
        ]
        

uploaded_file = st.file_uploader("Upload a file", type=["pdf"])
if uploaded_file is not None:
    import os
    # Create a 'uploads' directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    # Save the uploaded file to the 'uploads' directory
    file_path = os.path.join('uploads', uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    pdf_loader = PyPDFLoader('./uploads/' + uploaded_file.name)
    docs = pdf_loader.load()
    splitted_docs = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
        ).split_documents(docs)
    embeddings = MistralAIEmbeddings(api_key=mistral_api_key)
    db = Chroma.from_documents(
        splitted_docs,
        embeddings
    )
    retriever = db.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        "uploads_retriever",
        f"This tool searches through the uploaded document: {uploaded_file.name}. Use this tool to find information specific to the content of the uploaded file."
        )
    custom_tools.append(retriever_tool)
    llm_with_tools = llm.bind_tools(custom_tools)
    graph = graph_builder.compile()


# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI", avatar="./ib_logo.svg"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human", avatar="./user.jpg"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human", avatar="./user.jpg"):
        st.markdown(user_query)

    with st.chat_message("AI", avatar="./ib_logo.svg"):
        response = get_response(user_query, st.session_state.chat_history)
        st.write(response)

    st.session_state.chat_history.append(AIMessage(content=response))