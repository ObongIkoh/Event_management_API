from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID

from schemas.events import EventCreate, EventUpdate, Event
from services.events import EventService

# Create a global instance of EventService.
# This ensures that all routes use the same in-memory data store.
event_service_instance = EventService()

# Dependency function to provide the EventService instance to route handlers.
# FastAPI's Depends() will call this function to get the dependency.
def get_event_service() -> EventService:
    return event_service_instance

# Create an API router for event-related endpoints.
router = APIRouter(prefix="/events", tags=["Events"])
@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, event_service: EventService = Depends(get_event_service)):# Creates a new event. - **event**: EventCreate object with event details.
    return event_service.create_event(event)

#retrieves a single event by ID
@router.get("/{event_id}", response_model=Event)
def read_event(event_id: UUID, event_service: EventService = Depends(get_event_service)):
    event = event_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

#update an existing event
@router.put("/{event_id}", response_model=Event)
def update_event(event_id: UUID, update_data: EventUpdate, event_service: EventService = Depends(get_event_service)):
    updated = event_service.update_event(event_id, update_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return updated

#delete an event
@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: UUID, event_service: EventService = Depends(get_event_service)):
    deleted = event_service.delete_event(event_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return
# No content returned for 204 status

@router.get("/", response_model=List[Event])
def read_all_events(event_service: EventService = Depends(get_event_service)):
    # Retrieves all events.
    return event_service.get_all_events()
@router.patch("/{event_id}/deactivate", response_model=Event)
def deactivate_event(event_id: UUID, event_service: EventService = Depends(get_event_service)):
    event = event_service.deactivate_event(event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

#close registration for an event
@router.patch("/event/{event_id}/close_registration", response_model=Event)
def close_registration(event_id: UUID, event_service: EventService = Depends(get_event_service)):
    event = event_service.close_registration(event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event