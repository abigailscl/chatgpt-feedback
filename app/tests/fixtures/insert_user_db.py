import hashlib
import pytest
import boto3
from app.domain.models.person import Person

from app.domain.models.user import User


@pytest.fixture()
def insert_user_db(dynamodb_client, hash_password) -> User:
    def _insert_user_db(**kargs):
        hashed_password = hash_password(password=kargs["password"])
        dynamodb_client.put_item(
            TableName="FeedbackTable",
            Item={
                "user_email": {"S": kargs["email"]},
                "USER": {
                    "M": {
                        "email": {"S": kargs["email"]},
                        "password": {"S": hashed_password},
                        "name": {"S": kargs["name"]},
                    }
                },
                "FEEDBACK": {"M": {"peers": {"L": []}, "action_items": {"L": []}}},
            },
        )

        item = dynamodb_client.get_item(
            TableName="FeedbackTable", Key={"user_email": {"S": kargs["email"]}}
        )

        user_saved = item.get("Item").get("USER").get("M")
        email_saved = user_saved.get("email")["S"]
        person = Person(email=email_saved, name=user_saved.get("name")["S"])
        user = User(user=person, hashed_password=user_saved.get("password")["S"])

        return user

    return _insert_user_db


@pytest.fixture()
def hash_password() -> str:
    def _hash_password(password: str):
        hash_obj = hashlib.sha256()
        hash_obj.update(password.encode("utf-8"))
        return hash_obj.hexdigest()

    return _hash_password
