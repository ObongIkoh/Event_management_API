from fastapi import FastAPI
from routes import users, events, speakers, registrations


app = FastAPI(
    title= "Event Management API System"
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(speakers.router, prefix="/speakers", tags=["Speakers"])
app.include_router(registrations.router, prefix="/registrations", tags=["Registrations"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Event Management API System"}