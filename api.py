from fastapi import FastAPI
from pydantic import BaseModel
from trip_crew import generate_trip_plan
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TripMind AI Engine")

# This allows your future React frontend to talk to this API without security blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# This defines the exact data shape the frontend must send us
class TripRequest(BaseModel):
    destination: str
    travel_dates: str
    budget: str
    group_details: str


# This is the "Listener" that waits for the frontend to hit the "Generate" button
@app.post("/generate-itinerary")
def create_trip(request: TripRequest):
    print(f"Received request for {request.destination}...")

    # Trigger your CrewAI agents
    result = generate_trip_plan(
        group_details=request.group_details,
        destination=request.destination,
        budget=request.budget,
        travel_dates=request.travel_dates
    )

    # Send the final itinerary back to the frontend
    return {"itinerary": str(result)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)