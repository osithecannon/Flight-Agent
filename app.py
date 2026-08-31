import os
import requests
import streamlit as st

# Set page configuration to wide/dark theme style
st.set_page_config(
    page_title="Flight + Stay Agent", page_icon="✈️", layout="wide"
)

# Custom CSS to mimic the clean dark theme and amber search button
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .agent-tag {
        font-size: 11px;
        letter-spacing: 2px;
        color: #8b949e;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 0px;
    }
    .agent-title {
        font-size: 38px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 5px;
        margin-bottom: 10px;
    }
    .agent-subtitle {
        font-size: 14px;
        color: #8b949e;
        margin-bottom: 25px;
        line-height: 1.5;
    }
    .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }
    div.stButton > button {
        background-color: #f2a900 !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.5rem !important;
        border: none !important;
    }
    div.stButton > button:hover {
        background-color: #d99800 !important;
        color: #000000 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Local FastAPI background worker endpoint
api_url = "http://127.0.0.1:8001/plan"

# Main layout structure
col1, col2 = st.columns([1.6, 1])

with col1:
  st.markdown('<p class="agent-tag">FLIGHT + STAY AGENT</p>', unsafe_allow_html=True)
  st.markdown(
      '<h1 class="agent-title">Tell it where and when you’re free.</h1>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p class="agent-subtitle">Describe the trip in your own words. It reads'
      " your calendar, checks live fares and hotel rates, and reasons out its"
      " best pick.</p>",
      unsafe_allow_html=True,
  )

  # Text area prompt input
  user_prompt = st.text_area(
      "Trip prompt",
      placeholder=(
          "e.g. Find me a flight from Lagos to Abuja between September 1 and"
          " September 20"
      ),
      height=120,
      label_visibility="collapsed",
  )

  if st.button("Search"):
    if user_prompt.strip():
      with st.spinner(
          "Analyzing calendar, searching flights and finding hotels..."
      ):
        try:
          # Payload structured to satisfy the TravelRequest backend schema
          payload = {
              "prompt": user_prompt,
              "origin": "LOS",
              "destination": "ABV",
              "lat": 6.5244,
              "lng": 3.3792,
              "search_start": "2026-09-01",
              "search_end": "2026-09-20",
          }
          response = requests.post(api_url, json=payload, timeout=60)

          if response.status_code == 200:
            data = response.json()
            agent_reply = data.get("response", str(data))
            st.markdown("### Agent Recommendation")
            st.success(agent_reply)
          else:
            st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
          st.error(f"Failed to connect to backend agent: {e}")
    else:
      st.warning("Please enter a description for your trip first.")

with col2:
  st.markdown("")
