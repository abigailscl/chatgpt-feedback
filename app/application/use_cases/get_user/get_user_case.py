from app.domain.exceptions.user_not_found_error import UserNotFound
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository


class GetUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str) -> User:
        user = self.user_repository.get_by_email(email=email)
        if not user:
            raise UserNotFound(f"Not user found with this email: {email}")
        return user
