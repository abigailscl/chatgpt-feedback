from app.application.use_cases.register_user.request import RegisterUserRequest
from app.domain.exceptions.user_registration_error import UserRegistrationError
from app.domain.models.person import Person
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository


class RegisterUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, new_user: RegisterUserRequest) -> User:
        user_by_email = self.user_repository.get_by_email(new_user.email)
        if user_by_email:
            raise UserRegistrationError(
                f"The user with this email: {new_user.email}, already exists"
            )

        person = Person(**new_user.model_dump())
        hashed_password = self.user_repository.hash_password(
            new_pasword=new_user.password
        )
        user = User(user=person, hashed_password=hashed_password)
        registered_user = self.user_repository.save(user=user)

        return registered_user
