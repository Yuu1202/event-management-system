from fastapi import FastAPI
from app.presentation.routers import event_router, booking_router, refund_router, checkin_router

app = FastAPI(
    title="Event Management System",
    description="Event Ticketing & Booking System using Clean Architecture and DDD",
    version="1.0.0",
)

app.include_router(event_router.router)
app.include_router(booking_router.router)
app.include_router(refund_router.router)
app.include_router(checkin_router.router)


@app.get("/")
def root():
    return {"message": "Event Management System API"}