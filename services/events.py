from typing import List, Optional, Dict
from schemas.events import Event, EventCreate, EventUpdate
import uuid

class EventService:
    def __init__(self):
        self.events: List[Event] = []
        self.counter = 1

    def create_event(self, event_create: EventCreate) -> Event:
        event_data = event_create.model_dump() # Convert Pydantic model to dict, dict is deprecated in Pydantic v2
        event = Event(
            **event_data,
            id=uuid.uuid4()
        )
        self.events.append(event)
        return event

    def get_event(self, event_id: uuid.UUID) -> Optional[Event]:
        for event in self.events:
            if event.id == event_id:
                return event
        return None

    def update_event(self, event_id: uuid.UUID, event_update: EventUpdate) -> Optional[Event]:
        for index, event in enumerate(self.events):
            if event.id == event_id:
                updated_data = event.model_dump()
                updated_data.update(event_update.model_dump(exclude_unset=True))
                self.events[index] = Event(**updated_data)
                return self.events[index]
        return None

    def delete_event(self, event_id: uuid.UUID) -> bool:
        for index, event in enumerate(self.events):
            if event.id == event_id:
                del self.events[index]
                return True
        return False
    
    def close_event(self, event_id: uuid.UUID) -> Optional[Event]:
        for event in self.events:
            if event.id == event_id:
                event.is_active = False
                return event
        return None

    def get_all_events(self) -> List[Event]:
        return self.events