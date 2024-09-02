from faker import Faker
import pytest
from pytest_mock import MockerFixture
from app.application.use_cases.register_user.request import RegisterUserRequest
from app.domain.exceptions.user_registration_error import UserRegistrationError

from app.domain.models.person import Person
from app.domain.models.user import User
from app.application.use_cases.register_user.register_user_case import RegisterUser


faker = Faker()


class TestRegisterUser:
    def test__register_user__returns_user__when_user_create_an_account(
        self, mocker: MockerFixture
    ):
        email = faker.email()
        name = faker.name()
        password = faker.password()
        hashed_password = faker.password()
        person = Person(email=email, name=name)
        user = User(user=person, hashed_password=hashed_password)
        new_user = RegisterUserRequest(**person.model_dump(), password=password)
        user_repository = mocker.Mock(
            save=mocker.Mock(return_value=user),
            hash_password=mocker.Mock(return_value=hashed_password),
            get_by_email=mocker.Mock(return_value=None),
        )

        register_user_use_case = RegisterUser(user_repository=user_repository)
        registered_user = register_user_use_case.execute(new_user=new_user)

        user_repository.save.assert_called_once_with(user=user)
        user_repository.hash_password.assert_called_once_with(
            new_pasword=new_user.password
        )
        assert registered_user == user

    def test__register_user__raise_user_registration_exception__when_user_already_exists(
        self, mocker: MockerFixture
    ):
        email = faker.email()
        name = faker.name()
        password = faker.password()
        hashed_password = faker.password()
        person = Person(email=email, name=name)
        user = User(user=person, hashed_password=hashed_password)
        new_user = RegisterUserRequest(**person.model_dump(), password=password)
        user_repository = mocker.Mock(
            save=mocker.Mock(return_value=user),
            hash_password=mocker.Mock(return_value=hashed_password),
            get_by_email=mocker.Mock(return_value=user),
        )
        register_user_use_case = RegisterUser(user_repository=user_repository)
        error_message = f"The user with this email: {new_user.email}, already exists"

        with pytest.raises(UserRegistrationError) as exception_info:
            register_user_use_case.execute(new_user=new_user)

        assert str(exception_info.value) == error_message
