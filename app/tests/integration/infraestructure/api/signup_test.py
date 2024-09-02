from faker import Faker


fake = Faker()


def test__signup__returns_token__when_user_is_registered(
    mocker, client, setup_dynamodb
):
    email = fake.email()
    name = fake.name()
    password = fake.password()
    new_user = {"name": name, "email": email, "password": password}
    expected_user = {"name": name, "email": email}

    response = client.post("/signup", json=new_user)

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["user"] == expected_user
    assert json_response["hashed_password"] is not None


def test__signup__raise_not_found_exception__when_user_is_not_registered(
    mocker, client, setup_dynamodb, insert_user_db
):
    email = fake.email()
    name = fake.name()
    password = fake.password()
    insert_user_db(email=email, name=name, password=password)
    new_user = {"name": name, "email": email, "password": password}

    response = client.post("/signup", json=new_user)

    assert response.status_code == 400
    json_response = response.json()
    assert (
        json_response["message"] == f"The user with this email: {email}, already exists"
    )
