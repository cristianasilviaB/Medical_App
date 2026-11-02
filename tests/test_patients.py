def test_soft_delete_patient(client):
    # 1. Register and Login
    user_data = {"username": "patientadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Doctor
    doc_resp = client.post(
        "/doctors/",
        json={"name": "Dr. Smith", "specialization": "Cardiologie", "phone": "0711223344"},
        headers=headers,
    )
    doctor_id = doc_resp.json()["id"]

    # 3. Create Patient
    pat_resp = client.post(
        "/patients/",
        json={"name": "Ion Popescu", "age": 45, "disease": "Gripa", "doctor_id": doctor_id},
        headers=headers,
    )
    assert pat_resp.status_code == 201
    patient_id = pat_resp.json()["id"]
    assert pat_resp.json()["is_deleted"] is False

    # 4. Soft Delete Patient
    del_resp = client.delete(f"/patients/{patient_id}", headers=headers)
    assert del_resp.status_code == 200

    # 5. Verify patient does NOT appear in GET /patients/
    get_all_resp = client.get("/patients/")
    assert get_all_resp.status_code == 200
    assert len(get_all_resp.json()) == 0

    # 6. Verify GET /patients/{id} returns 404
    get_one_resp = client.get(f"/patients/{patient_id}")
    assert get_one_resp.status_code == 404


def test_get_patient_history(client):
    # 1. Register and Login
    user_data = {"username": "historyadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup Prerequisites
    doc_id = client.post(
        "/doctors/",
        json={"name": "Dr. History", "specialization": "General", "phone": "0799"},
        headers=headers,
    ).json()["id"]
    pat_id = client.post(
        "/patients/",
        json={"name": "Vasilescu Dan", "age": 50, "disease": "Diabet", "doctor_id": doc_id},
        headers=headers,
    ).json()["id"]
    srv_id = client.post(
        "/services/",
        json={"name": "Analize Sange", "price": 80.0, "duration_minutes": 15},
        headers=headers,
    ).json()["id"]

    # 3. Create Appointment
    client.post(
        "/appointments/",
        json={
            "patient_id": pat_id,
            "doctor_id": doc_id,
            "service_id": srv_id,
            "appointment_date": "2026-11-05T08:00:00",
        },
        headers=headers,
    )

    # 4. Fetch Patient History
    history_resp = client.get(f"/patients/{pat_id}/history")
    assert history_resp.status_code == 200
    assert history_resp.json()["name"] == "Vasilescu Dan"
    assert len(history_resp.json()["appointments"]) == 1