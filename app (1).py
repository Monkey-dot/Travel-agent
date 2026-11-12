import streamlit as st
from travel_agent import travel_agent_executor

st.set_page_config(page_title="AI Travel Assistant", layout="centered")
st.title("✈️ AI Travel Planning Assistant")
st.markdown("Enter your travel preferences, and our AI agent will autonomously build your personalized itinerary.")

with st.form("travel_form"):
    query = st.text_area("Describe your ideal trip:", 
                         placeholder="e.g., Plan a 3-day trip from Bangalore to Goa. I want a minimum 4-star hotel.")
    submitted = st.form_submit_button("Generate Itinerary")

if submitted and query:
    with st.spinner("Analyzing real-time data and building your itinerary..."):
        try:
            response = travel_agent_executor.invoke({"input": query})
            st.success("Your itinerary is ready!")
            st.markdown(response["output"])
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
