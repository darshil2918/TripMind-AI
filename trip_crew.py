import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# This loads your Groq API key securely from the .env file
load_dotenv()
# --- 1. THE AGENTS ---

demographic_profiler = Agent(
    role='Family Dynamics Specialist',
    goal='Analyze the group composition to identify specific constraints, energy levels, and needs.',
    backstory='You are an expert in family psychology and group travel. You know exactly what a 5-year-old needs versus a 60-year-old.',
    verbose=True
)

logistics_manager = Agent(
    role='Budget & Transport Director',
    goal='Find the best transport and accommodation that fits the fixed budget and the family constraints.',
    backstory='You are a frugal but clever travel agent. You know how to stretch a budget without sacrificing comfort.',
    verbose=True
)

experience_coordinator = Agent(
    role='Activity & Culinary Planner',
    goal='Create a daily itinerary with age-appropriate activities and local food options.',
    backstory='You are a local tour guide who knows the best spots that are both child-friendly and engaging for teenagers.',
    verbose=True
)

meteorologist = Agent(
    role='Weather & Preparation Expert',
    goal='Analyze expected weather for the dates and provide exact packing advice.',
    backstory='You are a veteran traveler and meteorologist who makes sure nobody is ever underprepared for the climate.',
    verbose=True
)

# --- 2. THE TASKS ---

profile_task = Task(
    description='Analyze the following travel group: {group_details}. Identify at least 3 critical constraints for this specific group.',
    expected_output='A bulleted list of group constraints (e.g., mobility limits, nap times).',
    agent=demographic_profiler
)

logistics_task = Task(
    description='Based on the constraints, plan transport and hotel recommendations for a trip to {destination} on a {budget} budget.',
    expected_output='A summary of the best transport method and a hotel recommendation that fits the budget.',
    agent=logistics_manager
)

activity_task = Task(
    description='Create a detailed daily itinerary for {destination} covering the dates: {travel_dates}. Balance activities for the group. YOU MUST RETURN ONLY A VALID JSON ARRAY.',
    expected_output='''A strict JSON array of objects, one for each day. Do not include markdown like ```json. Each day object MUST have this exact structure:
    {
      "id": "d1",
      "day": 1,
      "city": "Name of City",
      "theme": "Theme of the day",
      "highlights": ["Highlight 1", "Highlight 2"],
      "weather": "string, MUST be strictly 'sun' or 'cloud' based on forecast",
      "temp": "string, forecasted temperature (e.g., '22°' or '15°')",
      "timeline": [
        { "id": "b1", "time": "09:00", "title": "Breakfast", "place": "Local Cafe Name", "duration": "1h", "type": "meal" }
      ],
      "hidden_gems": [
        { "title": "Name of Hidden Gem", "subtitle": "Short description or distance" }
      ],
      "utilities": [
        { "name": "Local Pharmacy or Supermarket", "meta": "On route - 5 min walk" }
      ],
      "stays": [
        { "name": "Name of Hotel or Accommodation", "area": "Neighborhood", "price": "$150", "tag": "Best location", "rating": 4.8 }
      ],
      "transit": [
        { "label": "Local Transit Option", "price": "$15", "deal": "Day pass" }
      ],
      "dining": [
        { "name": "Restaurant Name", "tags": ["Cuisine", "Vibe"], "distance": "2 km", "price": "$$" }
      ]
    }''',
    agent=experience_coordinator
)

weather_task = Task(
    description='Provide weather-based packing advice for {destination} during the dates of {travel_dates}.',
    expected_output='A categorized packing list for the family.',
    agent=meteorologist
)


# --- 3. THE CREW ---

def generate_trip_plan(group_details, destination, budget, travel_dates):
    trip_crew = Crew(
        agents=[demographic_profiler, logistics_manager, experience_coordinator, meteorologist],
        tasks=[profile_task, logistics_task, weather_task, activity_task],
        process=Process.sequential  # They work in order, passing notes to each other
    )

    # This kicks off the AI process with the user's specific inputs
    result = trip_crew.kickoff(inputs={
        'group_details': group_details,
        'destination': destination,
        'budget': budget,
        'travel_dates': travel_dates
    })

    return result
