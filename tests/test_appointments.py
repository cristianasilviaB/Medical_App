def test_create_overlapping_appointment(client):
    # Register and Login
    user_data = {"username": "overlapadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Doctor, Patients, Service
    doc_id = client.post("/doctors/", json={"name": "Dr. Overlap", "specialization": "Cardiologie", "phone": "0700111222"}, headers=headers).json()["id"]
    pat1_id = client.post("/patients/", json={"name": "Patient 1", "age": 30, "disease": "None", "doctor_id": doc_id}, headers=headers).json()["id"]
    pat2_id = client.post("/patients/", json={"name": "Patient 2", "age": 40, "disease": "None", "doctor_id": doc_id}, headers=headers).json()["id"]
    srv_id = client.post("/services/", json={"name": "Consultation", "price": 150.0, "duration_minutes": 30}, headers=headers).json()["id"]

    now_iso = "2026-11-01T10:00:00"

    # Create First Appointment (10:00 - 10:30)
    resp1 = client.post(
        "/appointments/",
        json={"patient_id": pat1_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": now_iso},
        headers=headers,
    )
    assert resp1.status_code == 201

    #  Overlapping Appointment (10:15 - 10:45) -> Should Fail with HTTP 400
    overlap_iso = "2026-11-01T10:15:00"
    resp2 = client.post(
        "/appointments/",
        json={"patient_id": pat2_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": overlap_iso},
        headers=headers,
    )
    assert resp2.status_code == 400
    assert "not available" in resp2.json()["detail"].lower()