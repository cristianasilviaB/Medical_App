def test_get_services_empty(client):
    response = client.get("/services/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_service_unauthorized(client):
    service_data = {
        "name": "Consultatie Cardiologie",
        "price": 250.0,
        "duration_minutes": 30,
    }
    response = client.post("/services/", json=service_data)
    assert response.status_code == 401


def test_create_and_get_service(client):
    # register and login to get a token
    user_data = {"username": "serviceadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create a new medical service
    service_data = {
        "name": "Ecografie Generala",
        "price": 300.0,
        "duration_minutes": 45,
    }
    create_resp = client.post("/services/", json=service_data, headers=headers)
    assert create_resp.status_code == 201
    service_id = create_resp.json()["id"]
    assert create_resp.json()["name"] == "Ecografie Generala"

    # read all services and check that the new service is present
    get_all = client.get("/services/")
    assert get_all.status_code == 200
    assert len(get_all.json()) == 1

    # read the specific service by ID and check its details
    get_one = client.get(f"/services/{service_id}")
    assert get_one.status_code == 200
    assert get_one.json()["price"] == 300.0