def test_get_doctors_empty(client):
    response = client.get("/doctors/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_doctor_unauthorized(client):
    # Verificăm că încercarea de creare fără token JWT returnează 401 Unauthorized
    doctor_data = {
        "name": "Dr. Andrei Popescu",
        "specialization": "Cardiologie",
        "phone": "0712345678",
    }
    response = client.post("/doctors/", json=doctor_data)
    assert response.status_code == 401


def test_register_login_and_create_doctor(client):
    # 1. Înregistrare utilizator
    user_data = {"username": "testuser", "password": "testpassword123"}
    reg_resp = client.post("/auth/register", json=user_data)
    assert reg_resp.status_code == 201

    # 2. Autentificare pentru obținere token JWT
    login_resp = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword123"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # 3. Creare doctor cu Header-ul Authorization Bearer
    headers = {"Authorization": f"Bearer {token}"}
    doctor_data = {
        "name": "Dr. Elena Ionescu",
        "specialization": "Dermatologie",
        "phone": "0722334455",
    }
    doc_resp = client.post("/doctors/", json=doctor_data, headers=headers)
    assert doc_resp.status_code == 201
    assert doc_resp.json()["name"] == "Dr. Elena Ionescu"
    assert "id" in doc_resp.json()