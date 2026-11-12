import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from agent_tools import travel_tools

# Pull the API key securely from Streamlit Secrets
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

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
    ("placeholder", "{agent_scratchpad}"),
])

# Bind the tools to the agent
agent = create_tool_calling_agent(llm, travel_tools, prompt)

# Create the AgentExecutor which runs the agent loop
travel_agent_executor = AgentExecutor(agent=agent, tools=travel_tools, verbose=True)
