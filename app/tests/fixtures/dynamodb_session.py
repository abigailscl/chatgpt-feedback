from fastapi.testclient import TestClient
import pytest
import boto3

from app.infraestructure.api.main import app
from app.infraestructure.database.config.dynamodb import (
    create_table,
    delete_table,
    get_dynamodb_client,
)


@pytest.fixture
def dynamodb_client():
    yield boto3.client(
        "dynamodb", region_name="eu-west-1", endpoint_url="http://dynamodb-test:8000"
    )


@pytest.fixture()
def setup_dynamodb(dynamodb_client):
    create_table(dynamo_client=dynamodb_client)
    yield
    delete_table(dynamo_client=dynamodb_client)


@pytest.fixture
def client(dynamodb_client):
    def override_get_db():
        return dynamodb_client

    app.dependency_overrides[get_dynamodb_client] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
