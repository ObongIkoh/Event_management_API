from typing import List, Optional, Dict
from schemas.users import User, UserCreate, UserUpdate
import uuid
from datetime import date

class UserService:
    def __init__(self):
        self.users: List[User] = [] 
        

    def create_user(self, user_create: UserCreate) -> User:
        user_data = user_create.model_dump()
        user = User(
            **user_data, 
            id=uuid.uuid4()
            )
        self.users.append(user)
        return user

    def get_user(self, user_id: uuid.UUID) -> Optional[User]:
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    
    def get_all_users(self) -> List[User]:
        return self.users

    def update_user(self, user_id: uuid.UUID, user_update: UserUpdate) -> Optional[User]:
        for index, user in enumerate(self.users):
            if user.id == user_id:
                updated_data = user.model_dump()
                updated_data.update(user_update.model_dump(exclude_unset=True))
                self.users[index] = User(**updated_data)
                return self.users[index]
        return None

    def delete_user(self, user_id: uuid.UUID) -> bool:
        for index, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[index]
                return True
        return False

    def deactivate_user(self, user_id: uuid.UUID) -> Optional[User]: #deactivates a user by setting their is_active to false
        for user in self.users:
            if user.id == user_id:
                user.is_active = False
                return user
        return None