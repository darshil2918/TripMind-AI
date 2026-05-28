import streamlit as st
from trip_crew import generate_trip_plan

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="TripMind AI", page_icon="✈️", layout="centered")

# --- HEADER ---
st.title("✈️ TripMind AI")
st.subheader("Intelligent Group Travel Planner")
st.write("Plan a personalized trip that accommodates everyone—from 5-year-olds to grandparents, powered by an AI Crew!")
st.markdown("---")

# --- USER INPUT FORM ---
with st.form("trip_form"):
    destination = st.text_input("📍 Destination", placeholder="e.g., Bali, Indonesia or Coorg, Karnataka")
    travel_dates = st.text_input("📅 Travel Dates", placeholder="e.g., Dec 15 - Dec 22")
    budget = st.selectbox("💰 Budget Level", ["Economy (Budget-friendly)", "Standard (Mid-range)", "Luxury (High-end)"])

    group_details = st.text_area(
        "👨‍👩‍👧‍👦 Describe your travel group:",
        placeholder="e.g., 2 adults, a 5-year-old, 2 teenagers, and 2 grandparents in their 60s. Grandparents can't walk long distances."
    )

    # The submit button triggers the AI
    submitted = st.form_submit_button("Generate Trip Plan 🚀")

# --- AI EXECUTION ---
if submitted:
    if not destination or not travel_dates or not group_details:
        st.error("Please fill in all the details so the AI Crew can do their job!")
    else:
        # This spinner shows while the AI is thinking
        with st.spinner("🤖 The Profiler, Logistics Manager, and Coordinators are building your itinerary..."):
            try:
                # Call the function from your trip_crew.py file
                result = generate_trip_plan(group_details, destination, budget, travel_dates)

                # Print the final result to the screen
                st.success("Trip Plan Generated Successfully!")
                st.markdown("---")
                st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
