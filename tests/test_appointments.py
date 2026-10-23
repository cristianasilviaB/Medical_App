from datetime import datetime, timezone


def test_create_and_get_appointment(client):
    # Register and Login
    user_data = {"username": "apptadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Doctor
    doc_resp = client.post(
        "/doctors/",
        json={"name": "Dr. Maria Dan", "specialization": "Neurologie", "phone": "0733445566"},
        headers=headers,
    )
    doctor_id = doc_resp.json()["id"]

    # Create Patient
    pat_resp = client.post(
        "/patients/",
        json={"name": "Ana Radu", "age": 30, "disease": "Migrena", "doctor_id": doctor_id},
        headers=headers,
    )
    patient_id = pat_resp.json()["id"]

    # Create Medical Service
    srv_resp = client.post(
        "/services/",
        json={"name": "Consultatie Neurologie", "price": 200.0, "duration_minutes": 30},
        headers=headers,
    )
    service_id = srv_resp.json()["id"]

    # Create Appointment
    now_iso = datetime.now(timezone.utc).isoformat()
    appt_data = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "service_id": service_id,
        "appointment_date": now_iso,
    }
    create_resp = client.post("/appointments/", json=appt_data, headers=headers)
    assert create_resp.status_code == 201
    assert create_resp.json()["status"] == "scheduled"
    appt_id = create_resp.json()["id"]

    # Retrieve All Appointments
    get_all = client.get("/appointments/")
    assert get_all.status_code == 200
    assert len(get_all.json()) == 1

    # Retrieve One Appointment
    get_one = client.get(f"/appointments/{appt_id}")
    assert get_one.status_code == 200
    assert get_one.json()["id"] == appt_id