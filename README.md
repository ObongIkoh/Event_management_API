EVENT MANAGEMENT API SYSTEM
This projects implements a simple event management api which allows users to register for an event, track attendance, manage an event and speakers.
Each entity (User, Event, Registration, and Speaker) uses the CRUD method
FEATURES:
Users: Create, Read, Update, Delete, and Deactivate.
Event: Create,Read, Update, Delete, Deactivate, and Close registration.
Speakers: Create, Read, Update, and Delete. (Was initialized with three speakers).
Registration: Create, Read, Update, Delete, and Get users who attended at least one event
For data storage I used, inmemory list and dict for simplicity
Validation: Pydantic models are used for request and response validation.
Error Handling: Appropriate HTTP status codes are returned for all operations.

Modular Structure
routes/
    ├── __init__.py         # Initializes the routes package
    ├── user.py      # API endpoints for User
    ├── event.py     # API endpoints for Event
    ├── speaker.py   # API endpoints for Speaker
    └── registrations.py # API endpoints for Registration
schemas/
   ├── __init__.py         # Initializes the schemas package
   ├── users.py             # Pydantic models for User entity
   ├── events.py            # Pydantic models for Event entity
   ├── speakers.py          # Pydantic models for Speaker entity
   └── registrations.py     # Pydantic models for Registration entity
services/
   ├── __init__.py         # Initializes the services package
   ├── users.py     # Business logic for User operations
   ├── events.py    # Business logic for Event operations
   ├── speakers.py  # Business logic for Speaker operations (with initial data)
   └── registrations.py # Business logic for Registration operations
main.py

How to Run the Application
Prerequisites
Make sure you have Python 3.9+ installed.
Installation
Clone the repository:
git clone <YOUR_GITHUB_REPO_URL>
cd event-management-api
(Replace <YOUR_GITHUB_REPO_URL> with the actual URL of your public GitHub repository after pushing your code.)
Create a virtual environment (recommended): python -m venv env
Activate the virtual environment:
On Windows:
.\env\Scripts\activate
on GitBash
source env/Scripts/activate
Install dependencies: pip install "fastapi[all]" uvicorn pydantic
Running the API
Start the FastAPI application using Uvicorn: uvicorn main:app --reload
The --reload flag will automatically restart the server on code changes.
Access the API Documentation:
Once the server is running, you can access the interactive API documentation (Swagger UI) at:
http://127.0.0.1:8000/docs
Or the ReDoc documentation at:
http://127.0.0.1:8000/redoc

Users Endpoint
GET/users/Users/: Read All Users
POST/users/Users/: Create User
GET/users/Users/{user_id}: Read User
PUT/users/Users/{user_id}: Update User
DELETE/users/Users/{user_id}: Delete User
PATCH/users/Users/users/{user_id}/deactivate: Deactivate User

Events Endpoint
GET/events/events/:Read All Events
POST/events/events/: Create Event
GET/events/events/{event_id}: Read Event
PUT/events/events/{event_id}:Update Event
DELETE/events/events/{event_id}:Delete Event
PATCH/events/events/{event_id}/deactivate:Deactivate Event
PATCH/events/events/event/{event_id}/close_registration:Close Registration

Speakers Endpoint
POST/speakers/speakers/:Create Speaker
GET/speakers/speakers/speakers/{speaker_id}: Read Speaker
PUT/speakers/speakers/speakers/{speaker_id}:Update Speaker
DELETE/speakers/speakers/speakers/{speaker_id}:Delete Speaker
GET/speakers/speakers/speakers/:Read All Speakers

Registrations Endpoint
GET/registrations/registrations/: Read All Registrations
POST/registrations/registrations/:Create Registration
1. Requires the user to be is_active=True.
2. Requires the event to be is_open=True.
3. Prevents duplicate registrations (same user, same event).
PATCH/registrations/registrations/{registration_id}/attendance:Update Attendance
GET/registrations/registrations/{registration_id}:Read Registration
DELETE/registrations/registrations/{registration_id}:Delete Registration
GET/registrations/registrations/user/{user_id}:Get registration for a particular user
GET/registrations/registrations/attended/users:Get Users Who Attended At Least One Event
GET/registrations/registrations/event/{event_id}:Get registration for a particular event
