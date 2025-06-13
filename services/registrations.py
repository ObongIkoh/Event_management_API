import uuid
from typing import List, Optional, Dict
from datetime import datetime
from schemas.registrations import Registration, RegistrationCreate, RegistrationUpdate
from schemas.users import User
from services.users import UserService
from services.events import  EventService

class RegistrationService:
    def __init__(self, user_service: UserService, event_service: EventService):
        self.registrations: List[Registration] = []
        self.user_service = user_service
        self.event_service = event_service
        
    def register_user(self, registration: RegistrationCreate) -> Registration:
        user = self.user_service.get_user(registration.user_id)
    
    #check if user exists and is active
        if not user:
            raise ValueError("Invalid user ID")
        if not user.is_active:
            raise ValueError("User is not active")
    
    #event check
        event = self.event_service.get_event(registration.event_id)
        if not event:
            raise ValueError("Invalid event ID")
        if not event.is_active:
            raise ValueError("Event is not active")
    
    #check if user is already registered for the event
        for reg in self.registrations:
            if reg.user_id == registration.user_id and reg.event_id == registration.event_id:
                raise ValueError("User is already registered for this event")
        
        new_registration = Registration(
            id=str(uuid.uuid4()),  # Generate a unique ID for the registration
            user_id=registration.user_id,
            event_id=registration.event_id,
            registration_date=datetime.now(),
            attended = False,  # Default to False
        )
        self.registrations.append(new_registration)
        return new_registration

    def get_registration() -> List[Registration]:
        return Registration
    
    def get_registrations_for_user(self, user_id: str) -> List[Registration]:
        return [reg for reg in self.registrations if reg.user_id == user_id]
    
    def get_registration(self, registration_id: str) -> Optional[Registration]:
        for reg in self.registrations:
            if reg.id == registration_id:
                return reg
        return None

    def get_all_registrations(self) -> List[Registration]:
        return self.registrations
    
    def get_user_registrations(self, user_id: str) -> List[Registration]:
        return [reg for reg in self.registrations if reg.user_id == user_id]
    
    def get_users_attended_at_least_one_event(self) -> List[User]:
        attended_user_ids = set() # Use a set to avoid duplicates
        for reg in self.registrations:
            if reg.attended:
                attended_user_ids.add(reg.user_id)
        
        attended_users = []
        for user_id in attended_user_ids:
            user = self.user_service.get_user(user_id)
            if user:
                attended_users.append(user)
        return attended_users
    
    def mark_attendance(self, registration_id: str) -> Optional[Registration]:
        registration = self.registrations.get(registration_id)
        if registration:
            registration.attended = True # Set attended status to True
            self.registrations[registration_id] = registration # Update in storage
        return registration
    