from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID

from schemas.registrations import RegistrationCreate, RegistrationUpdate, Registration
from schemas.users import User  # Import User schema/model
from services.registrations import RegistrationService
from services.users import UserService
# Importing the RegistrationService and UserService to handle registration logic.
from services.events import EventService

# Create a global instance of RegistrationService.
user_service_instance = UserService()
event_service_instance = EventService()
registration_service_instance = RegistrationService(user_service=user_service_instance, event_service=event_service_instance)
# This ensures that all routes use the same in-memory data store.

#dependency function to provide the RegistrationService instance to route handlers.
def get_registration_service_dependency() -> RegistrationService:
    return registration_service_instance

#router with base path and tags 
router = APIRouter(prefix="/registrations", tags=["Registrations"])
@router.post("/", response_model=Registration, status_code=status.HTTP_201_CREATED)
def create_registration(
    registration: RegistrationCreate,
    reg_service: RegistrationService = Depends(get_registration_service_dependency)
):
    result = reg_service.register_user_for_event(registration)
    if isinstance(result, str):
        if "User not found" in result or "Event not found" in result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result)
        elif "User is not active" in result or "Event registration is closed" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result)
        elif "User already registered" in result:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=result)
    return result

@router.patch("/{registration_id}/attendance", response_model=Registration)
def update_attendance(
    registration_id: UUID,
    attendance: bool,
    reg_service: RegistrationService = Depends(get_registration_service_dependency)
):
    result = reg_service.update_attendance(registration_id, attendance)
    if isinstance(result, str):
        if "Registration not found" in result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result)
        elif "Invalid attendance status" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result)
    return result

@router.get("/{registration_id}", response_model=Registration)
def read_registration(registration_id: UUID, registration_service: RegistrationService = Depends(get_registration_service_dependency)):
    registration = registration_service.get_registration(registration_id)
    if not registration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
    return registration

@router.get("/user/{user_id}", response_model=List[Registration])
def read_user_registrations(
    user_id: str,
    reg_service: RegistrationService = Depends(get_registration_service_dependency)
):
    return reg_service.get_registrations_for_user(user_id)

@router.get("/", response_model=List[Registration])
def read_all_registrations(
    reg_service: RegistrationService = Depends(get_registration_service_dependency)
):
    return reg_service.get_all_registrations()

@router.get("/attended/users", response_model=List[User])
def get_users_who_attended_at_least_one_event(
    reg_service: RegistrationService = Depends(get_registration_service_dependency)
):
    return reg_service.get_users_who_attended_at_least_one_event()

@router.get("/event/{event_id}", response_model=List[Registration])
def read_event_registrations(
    event_id: str,
    reg_service: RegistrationService = Depends(get_registration_service_dependency)
):
    return reg_service.get_registrations_for_event(event_id)

@router.delete("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_registration(
    registration_id: UUID,
    reg_service: RegistrationService = Depends(get_registration_service_dependency)
):
    if not reg_service.delete_registration(registration_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
    return