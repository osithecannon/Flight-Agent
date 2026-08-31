import os
import requests
import streamlit as st

st.set_page_config(
    page_title="Flight & Stay Agent", page_icon="✈️", layout="centered"
)

st.title("✈️ Groq-Powered Flight & Stay Agent")
st.markdown("Search flights dynamically by location, dates, and class.")

# Permanently use the local background FastAPI worker endpoint (No sidebar box needed!)
api_url = "http://127.0.0.1:8001/plan"

# Sidebar for structured search parameters
st.sidebar.header("Flight Search Parameters")
origin = st.sidebar.text_input("Origin Airport (e.g., LOS)", value="LOS")
destination = st.sidebar.text_input("Destination Airport (e.g., LHR)", value="LHR")
departure_date = st.sidebar.date_input("Departure Date")
cabin = st.sidebar.selectbox(
    "Cabin Class", ["economy", "premium_economy", "business", "first"]
)

use_sidebar_search = st.sidebar.checkbox("Use Structured Search Form", value=True)

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

trigger_search = False
prompt = ""

if use_sidebar_search:
  if st.sidebar.button("Search Flights & Plan"):
    prompt = f"Find a {cabin} flight from {origin} to {destination} on {departure_date}. Add it to my calendar."
    trigger_search = True
else:
  prompt = st.chat_input("e.g., Find me a flight from Lagos to London next Monday")
  if prompt:
    trigger_search = True

if trigger_search and prompt:
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    with st.spinner("Searching Duffel and talking to your calendar..."):
      try:
        payload = {"prompt": prompt}
        response = requests.post(api_url, json=payload, timeout=60)

        if response.status_code == 200:
          data = response.json()
          agent_reply = data.get("response", str(data))
          st.markdown(agent_reply)
          st.session_state.messages.append(
              {"role": "assistant", "content": agent_reply}
          )
        else:
          st.error(f"Error {response.status_code}: {response.text}")
      except Exception as e:
        st.error(f"Failed to connect to the agent endpoint. Details: {e}")
