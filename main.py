from fastapi import FastAPI

app = FastAPI(
    title="Event Management System",
    description="Event Ticketing & Booking System using Clean Architecture and DDD",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "Event Management System API"}