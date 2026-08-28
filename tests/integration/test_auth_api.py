from fastapi.testclient import TestClient


def test_auth_register_success(client: TestClient):
    response = client.post(
        "/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "Password123!",
            "role": "user",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "user"
    assert data["is_active"] is True
    assert "password" not in data
    assert "hashed_password" not in data


def test_auth_register_duplicate(client: TestClient):
    payload = {
        "email": "duplicate@example.com",
        "password": "Password123!",
    }
    res1 = client.post("/v1/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/v1/auth/register", json=payload)
    assert res2.status_code == 400
    assert res2.json()["code"] == "ALREADY_EXISTS"


def test_auth_register_short_password(client: TestClient):
    response = client.post(
        "/v1/auth/register",
        json={
            "email": "short@example.com",
            "password": "short",
        },
    )
    assert response.status_code == 422


def test_auth_login_success(client: TestClient):
    client.post(
        "/v1/auth/register",
        json={"email": "login@example.com", "password": "Password123!"},
    )

    response = client.post(
        "/v1/auth/login",
        json={"email": "login@example.com", "password": "Password123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_auth_login_wrong_password(client: TestClient):
    client.post(
        "/v1/auth/register",
        json={"email": "wrongpass@example.com", "password": "Password123!"},
    )

    response = client.post(
        "/v1/auth/login",
        json={"email": "wrongpass@example.com", "password": "WrongPassword!"},
    )
    assert response.status_code == 401
    assert response.json()["code"] == "UNAUTHORIZED"


def test_auth_refresh_flow(client: TestClient):
    client.post(
        "/v1/auth/register",
        json={"email": "refresh@example.com", "password": "Password123!"},
    )
    login_res = client.post(
        "/v1/auth/login",
        json={"email": "refresh@example.com", "password": "Password123!"},
    )
    refresh_token = login_res.json()["refresh_token"]

    refresh_res = client.post(
        "/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_res.status_code == 200
    data = refresh_res.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_auth_me_endpoint(client: TestClient):
    client.post(
        "/v1/auth/register",
        json={
            "email": "me@example.com",
            "password": "Password123!",
            "role": "admin",
        },
    )
    login_res = client.post(
        "/v1/auth/login",
        json={"email": "me@example.com", "password": "Password123!"},
    )
    access_token = login_res.json()["access_token"]

    # 1. Successful /me
    me_res = client.get(
        "/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "me@example.com"
    assert me_res.json()["role"] == "admin"

    # 2. Missing authorization header -> 401
    unauth_res = client.get("/v1/auth/me")
    assert unauth_res.status_code == 401

    # 3. Invalid token -> 401
    invalid_res = client.get(
        "/v1/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"},
    )
    assert invalid_res.status_code == 401
