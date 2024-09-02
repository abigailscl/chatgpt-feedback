from faker import Faker


fake = Faker()


def test__login__returns_token__when_user_is_registered(
    mocker, client, setup_dynamodb, insert_user_db
):
    email = fake.email()
    name = fake.name()
    password = fake.password()
    user_registered = insert_user_db(email=email, name=name, password=password)

    response = client.post(
        "/login", data={"username": user_registered.user.email, "password": password}
    )

    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"


def test__login__raise_not_found_exception__when_user_is_not_registered(
    mocker, client, setup_dynamodb
):
    email = fake.email()
    password = fake.password()

    response = client.post("/login", data={"username": email, "password": password})

    assert response.status_code == 404
    json_response = response.json()
    assert json_response["message"] == f"Not user found with this email: {email}"


def test__login__raise_invalid_password_exception__when_password_is_invalid(
    mocker, client, setup_dynamodb, insert_user_db
):
    email = fake.email()
    name = fake.name()
    password = fake.password()
    user_registered = insert_user_db(email=email, name=name, password=password)

    response = client.post(
        "/login",
        data={"username": user_registered.user.email, "password": fake.password()},
    )

    assert response.status_code == 400
    json_response = response.json()
    assert json_response["message"] == "Invalid password"
