from faker import Faker
import pytest
from pytest_mock import MockerFixture
from app.application.use_cases.authenticate_user.authenticate_user import (
    AuthenticateUser,
)
from app.application.use_cases.authenticate_user.request import AuthenticaeUserRequest
from app.domain.exceptions.invalid_password_error import InvalidPasword
from app.domain.exceptions.user_not_found_error import UserNotFound

from app.domain.models.person import Person
from app.domain.models.user import User


faker = Faker()


class TestAuhenticateUser:
    def test__authenticate_user__returns_user__when_email_is_registered(
        self, mocker: MockerFixture
    ):
        email = faker.email()
        name = faker.name()
        hashed_password = faker.password()
        person = Person(email=email, name=name)
        user = User(user=person, hashed_password=hashed_password)
        authenticate_user_request = AuthenticaeUserRequest(
            email=user.user.email,
            password=user.hashed_password,
            hashed_password=hashed_password,
        )
        user_repository = mocker.Mock(get_by_email=mocker.Mock(return_value=user))

        authenticate_user_case = AuthenticateUser(user_repository=user_repository)
        response_user = authenticate_user_case.execute(
            authenticate_user_request=authenticate_user_request
        )

        assert response_user == user

    def test__authenticate_user__raise_user_not_found_exception__when_email_is_not_registered(
        self, mocker: MockerFixture
    ):
        email = faker.email()
        password = faker.password()
        authenticate_user_request = AuthenticaeUserRequest(
            email=email, password=password, hashed_password=password
        )
        error_message = (
            f"Not user found with this email: {authenticate_user_request.email}"
        )
        user_repository = mocker.Mock(get_by_email=mocker.Mock(return_value=None))

        authenticate_user_case = AuthenticateUser(user_repository=user_repository)
        with pytest.raises(UserNotFound) as exception_info:
            authenticate_user_case.execute(
                authenticate_user_request=authenticate_user_request
            )

        assert str(exception_info.value) == error_message

    def test__authenticate_user__raise_invalid_pasword_exception__when_email_is_not_registered(
        self, mocker: MockerFixture
    ):
        email = faker.email()
        name = faker.name()
        hashed_password = faker.password()
        authenticate_user_request = AuthenticaeUserRequest(
            email=email, password=hashed_password, hashed_password=hashed_password
        )
        person = Person(email=email, name=name)
        user = User(user=person, hashed_password=hashed_password)
        error_message = "Invalid password"
        user_repository = mocker.Mock(
            get_by_email=mocker.Mock(return_value=user),
            verify_password=mocker.Mock(return_value=None),
        )

        authenticate_user_case = AuthenticateUser(user_repository=user_repository)
        with pytest.raises(InvalidPasword) as exception_info:
            authenticate_user_case.execute(
                authenticate_user_request=authenticate_user_request
            )

        assert str(exception_info.value) == error_message
