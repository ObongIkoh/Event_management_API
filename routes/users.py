from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID

from schemas.users import UserCreate, UserUpdate, User
from services.users import UserService

# Create a global instance of UserService.
# This ensures that all routes use the same in-memory data store.
user_service_instance = UserService()

# Dependency function to provide the UserService instance to route handlers.
# FastAPI's Depends() will call this function to get the dependency.
def get_user_service() -> UserService:
    return user_service_instance

# Create an API router for user-related endpoints.
router = APIRouter(prefix="/Users", tags=["Users"])
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user) #creates a new user

@router.get("/{user_id}", response_model=User)
def read_user(user_id: UUID, user_service: UserService = Depends(get_user_service)): #retrieves a single user by ID
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/", response_model=List[User])
def read_all_users(user_service: UserService = Depends(get_user_service)): #retrieves all users by list
    return user_service.get_all_users()

@router.put("/{user_id}", response_model=User)
def update_user(user_id: UUID, user_update: UserUpdate, user_service: UserService = Depends(get_user_service)):

    # Updates an existing user's information.
    # - **user_id**: The ID of the user to update.
    # - **user_update**: UserUpdate object with fields to be updated.
    # - Raises 404 if the user is not found.
    
    user = user_service.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    if not user_service.delete_user(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return # No content returned for 204 status

@router.patch("/users/{user_id}/deactivate", response_model=User)
def deactivate_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    # Deactivates a user (sets is_active to False).
    # - **user_id**: The ID of the user to deactivate.
    # - Raises 404 if the user is not found.
    user = user_service.deactivate_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

