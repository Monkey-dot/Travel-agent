import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
# Import from langchain.agents.format_scratchpad.tools instead of langchain.agents
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.tools import format_to_tool_messages
from langchain.agents.output_parsers.tools import ToolsAgentOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from agent_tools import travel_tools

# Pull the API key securely from Streamlit Secrets
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Bind tools to LLM
llm_with_tools = llm.bind_tools(travel_tools)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert Indian travel planning assistant. 
    Your job is to build a complete 3-7 day itinerary based on user preferences.
    
    You have access to the following tools:
    - search_flights: Find the cheapest flight.
    - search_hotels: Find top-rated accommodations.
    - search_places: Find attractions to visit.
    - get_weather: Get the weather forecast for the destination.
    - estimate_budget: Calculate the total trip cost in INR.
    
    You must use these tools to gather real data. Do not invent prices or places.
    
    Format your final response strictly as follows:
    **Your [Number]-Day Trip to [Destination]**
    
    **Flight Selected:**
    - [Airline] (₹[Price]) – Departs [Source] at [Time]
    
    **Hotel Booked:**
    - [Hotel Name] (₹[Price]/night, [Stars]-star)
    
    **Weather:**
    - [Weather Data from tool]
    
    **Itinerary:**
    - Day 1: [Place 1], [Place 2]
    - Day 2: [Place 3], [Place 4]
    
    **Estimated Total Budget:**
    - Flight: ₹[Cost]
    - Hotel: ₹[Cost]
    - Food & Travel: ₹[Cost]
    -------------------------------------
    **Total Cost: ₹[Cost]**
    """),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Manually construct the tool calling agent (this avoids the import error)
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_tool_messages(x["intermediate_steps"]),
    }
    | prompt
    | llm_with_tools
    | ToolsAgentOutputParser()
)

travel_agent_executor = AgentExecutor(agent=agent, tools=travel_tools, verbose=True)
