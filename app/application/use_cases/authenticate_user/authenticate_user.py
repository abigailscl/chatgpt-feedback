from app.domain.exceptions.invalid_password_error import InvalidPasword
from app.domain.models.user import User
from .request import AuthenticaeUserRequest
from app.domain.exceptions.user_not_found_error import UserNotFound
from app.domain.repositories.user_repository import UserRepository


class AuthenticateUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, authenticate_user_request: AuthenticaeUserRequest) -> User:
        user = self.user_repository.get_by_email(authenticate_user_request.email)
        if not user:
            raise UserNotFound(
                f"Not user found with this email: {authenticate_user_request.email}"
            )
        if not self.user_repository.verify_password(
            authenticate_user_request.hashed_password, authenticate_user_request.email
        ):
            raise InvalidPasword("Invalid password")
        return user
