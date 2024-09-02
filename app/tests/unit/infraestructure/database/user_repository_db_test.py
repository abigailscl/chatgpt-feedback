from faker import Faker
import pytest
from botocore.exceptions import ClientError

from app.domain.exceptions.user_registration_error import UserRegistrationError
from app.domain.models.person import Person
from app.domain.models.user import User
from app.infraestructure.database.user_repository_db import UserRepositoryDB


faker = Faker()


class TestUserRepositoryDB:
    def test__save__returns_user__when_dyamobd_registers_succesfully(
        self, dynamodb_client, setup_dynamodb
    ):
        session = dynamodb_client
        email = faker.email()
        name = faker.name()
        hashed_password = faker.password()
        person = Person(email=email, name=name)
        user = User(user=person, hashed_password=hashed_password)

        user_repository_db = UserRepositoryDB(session=session)
        saved_user = user_repository_db.save(user=user)

        assert saved_user == user

    def test__save__raise_user_registration_error__when_dyamobd_failed(
        self, mocker, setup_dynamodb
    ):
        email = faker.email()
        name = faker.name()
        hashed_password = faker.password()
        person = Person(email=email, name=name)
        new_user = User(user=person, hashed_password=hashed_password)
        error_message = f"Error inserting this user {new_user.user.email} into the DB"
        mock_boto_client = mocker.patch("boto3.client")
        mock_dynamodb = mock_boto_client.return_value
        mock_dynamodb.put_item.side_effect = UserRegistrationError(error_message)

        user_repository_db = UserRepositoryDB(session=None)
        with pytest.raises(UserRegistrationError) as exception_info:
            user_repository_db.save(user=new_user)

        assert str(exception_info.value) == error_message

    def test__hash_password__returns_hashed_password__when_sends_password(
        self, dynamodb_client, setup_dynamodb
    ):
        session = dynamodb_client
        password = faker.password()

        user_repository_db = UserRepositoryDB(session=session)
        hashed_password = user_repository_db.hash_password(password)

        assert hashed_password is not None

    def test__hash_password__returns_user__when_email_is_registered(
        self, dynamodb_client, setup_dynamodb, insert_user_db
    ):
        session = dynamodb_client
        email = faker.email()
        name = faker.name()
        password = faker.password()
        insert_user_db(email=email, name=name, password=password)

        user_repository_db = UserRepositoryDB(session=session)
        user = user_repository_db.get_by_email(email=email)

        assert user.user.email == email

    def test__hash_password__returns_user__when_email_is_not_registered(
        self, dynamodb_client, setup_dynamodb
    ):
        session = dynamodb_client
        email = faker.email()

        user_repository_db = UserRepositoryDB(session=session)
        user = user_repository_db.get_by_email(email=email)

        assert user is None

    def test__hash_password__returns_true__when_password_is_registered(
        self, dynamodb_client, setup_dynamodb, insert_user_db, hash_password
    ):
        session = dynamodb_client
        email = faker.email()
        name = faker.name()
        password = faker.password()
        hashed_password = hash_password(password=password)
        insert_user_db(email=email, name=name, password=password)

        user_repository_db = UserRepositoryDB(session=session)
        response = user_repository_db.verify_password(
            hashed_password=hashed_password, email=email
        )

        assert response

    def test__hash_password__returns_false__when_password_is_not_registered(
        self, dynamodb_client, setup_dynamodb, hash_password
    ):
        session = dynamodb_client
        email = faker.email()
        password = faker.password()
        hashed_password = hash_password(password=password)

        user_repository_db = UserRepositoryDB(session=session)
        response = user_repository_db.verify_password(
            hashed_password=hashed_password, email=email
        )

        assert not response
