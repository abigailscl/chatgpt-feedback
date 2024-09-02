import pytest

from faker import Faker
from pytest_mock import MockerFixture
from app.application.use_cases.get_user.get_user_case import GetUser
from app.domain.exceptions.user_not_found_error import UserNotFound

from app.domain.models.person import Person
from app.domain.models.user import User


faker = Faker()


class TestGetUser:
    def test__get_user_by_email__returns_user__when_email_is_registered(
        self, mocker: MockerFixture
    ):
        email = faker.email()
        name = faker.name()
        hashed_password = faker.password()
        person = Person(email=email, name=name)
        user = User(user=person, hashed_password=hashed_password)
        user_repository = mocker.Mock(get_by_email=mocker.Mock(return_value=user))

        get_user_case = GetUser(user_repository=user_repository)
        response_user = get_user_case.execute(email=email)

        user_repository.get_by_email.assert_called_once_with(email=email)
        assert response_user == user

    def test__get_user_by_email__raise_user_not_found_exception__when_email_is_not_registered(
        self, mocker: MockerFixture
    ):
        email = faker.email()
        error_message = f"Not user found with this email: {email}"
        user_repository = mocker.Mock(get_by_email=mocker.Mock(return_value=None))

        get_user_case = GetUser(user_repository=user_repository)
        with pytest.raises(UserNotFound) as exception_info:
            get_user_case.execute(email=email)

        assert str(exception_info.value) == error_message
