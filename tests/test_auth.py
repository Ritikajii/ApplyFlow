
def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


def test_register_duplicate_user(client):
    user_data = {
        "email": "test@example.com",
        "password": "TestPass123"
    }

    client.post("/auth/register", json=user_data)

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 409


def test_login_user(client):
    user_data = {
        "email": "test@example.com",
        "password": "TestPass123"
    }

    client.post("/auth/register", json=user_data)

    response = client.post("/auth/login", json=user_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPass123"
        }
    )

    assert response.status_code == 401
