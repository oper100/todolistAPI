def test_register(client):
    response = client.post(
        "/auth/register", json={"username": "alice", "password": "password123"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "alice"
    assert "password" not in body
    assert "hashed_password" not in body


def test_register_duplicate_username(client):
    payload = {"username": "alice", "password": "password123"}
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409


def test_register_short_password(client):
    response = client.post(
        "/auth/register", json={"username": "alice", "password": "short"}
    )
    assert response.status_code == 422


def test_login(client):
    client.post("/auth/register", json={"username": "alice", "password": "password123"})
    response = client.post(
        "/auth/token", data={"username": "alice", "password": "password123"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "alice", "password": "password123"})
    response = client.post(
        "/auth/token", data={"username": "alice", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_login_unknown_user(client):
    response = client.post(
        "/auth/token", data={"username": "nobody", "password": "password123"}
    )
    assert response.status_code == 401


def test_todos_require_token(client):
    assert client.get("/todos/").status_code == 401


def test_todos_reject_invalid_token(client):
    response = client.get("/todos/", headers={"Authorization": "Bearer garbage"})
    assert response.status_code == 401
