def test_create_overlapping_appointment(client):
    # 1. Register and Login
    user_data = {"username": "overlapadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Doctor, Patients, Service
    doc_id = client.post(
        "/doctors/",
        json={"name": "Dr. Overlap", "specialization": "Cardiologie", "phone": "0700111222"},
        headers=headers,
    ).json()["id"]
    pat1_id = client.post(
        "/patients/",
        json={"name": "Patient 1", "age": 30, "disease": "None", "doctor_id": doc_id},
        headers=headers,
    ).json()["id"]
    pat2_id = client.post(
        "/patients/",
        json={"name": "Patient 2", "age": 40, "disease": "None", "doctor_id": doc_id},
        headers=headers,
    ).json()["id"]
    srv_id = client.post(
        "/services/",
        json={"name": "Consultation", "price": 150.0, "duration_minutes": 30},
        headers=headers,
    ).json()["id"]

    now_iso = "2026-11-01T10:00:00"

    # 3. Create First Appointment (10:00 - 10:30)
    resp1 = client.post(
        "/appointments/",
        json={"patient_id": pat1_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": now_iso},
        headers=headers,
    )
    assert resp1.status_code == 201

    # 4. Try Overlapping Appointment (10:15 - 10:45) -> Should Fail with HTTP 400
    overlap_iso = "2026-11-01T10:15:00"
    resp2 = client.post(
        "/appointments/",
        json={"patient_id": pat2_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": overlap_iso},
        headers=headers,
    )
    assert resp2.status_code == 400
    assert "not available" in resp2.json()["detail"].lower()


def test_update_appointment_status(client):
    # 1. Register and Login
    user_data = {"username": "statusadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup Prerequisites
    doc_id = client.post(
        "/doctors/",
        json={"name": "Dr. Status", "specialization": "Dermatologie", "phone": "0711"},
        headers=headers,
    ).json()["id"]
    pat_id = client.post(
        "/patients/",
        json={"name": "Maria", "age": 25, "disease": "Acnee", "doctor_id": doc_id},
        headers=headers,
    ).json()["id"]
    srv_id = client.post(
        "/services/",
        json={"name": "Consult", "price": 120.0, "duration_minutes": 20},
        headers=headers,
    ).json()["id"]

    now_iso = "2026-12-01T14:00:00"
    appt = client.post(
        "/appointments/",
        json={"patient_id": pat_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": now_iso},
        headers=headers,
    ).json()

    # 3. Update status to 'completed'
    update_resp = client.patch(f"/appointments/{appt['id']}/status", json={"status": "completed"}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "completed"

    # 4. Try updating to an invalid status -> Should return HTTP 400
    invalid_resp = client.patch(
        f"/appointments/{appt['id']}/status",
        json={"status": "invalid_status"},
        headers=headers,
    )
    assert invalid_resp.status_code == 400


def test_cancelled_appointment_frees_slot(client):
    # 1. Register and Login
    user_data = {"username": "freeslotadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup Prerequisites
    doc_id = client.post(
        "/doctors/",
        json={"name": "Dr. Free", "specialization": "Pediatrie", "phone": "0722"},
        headers=headers,
    ).json()["id"]
    pat1_id = client.post(
        "/patients/",
        json={"name": "Copil 1", "age": 5, "disease": "Gripa", "doctor_id": doc_id},
        headers=headers,
    ).json()["id"]
    pat2_id = client.post(
        "/patients/",
        json={"name": "Copil 2", "age": 8, "disease": "Tuse", "doctor_id": doc_id},
        headers=headers,
    ).json()["id"]
    srv_id = client.post(
        "/services/",
        json={"name": "Consult", "price": 100.0, "duration_minutes": 30},
        headers=headers,
    ).json()["id"]

    slot_iso = "2026-12-10T09:00:00"

    # 3. Create appointment 1
    appt1 = client.post(
        "/appointments/",
        json={"patient_id": pat1_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": slot_iso},
        headers=headers,
    ).json()

    # 4. Cancel appointment 1
    client.patch(f"/appointments/{appt1['id']}/status", json={"status": "cancelled"}, headers=headers)

    # 5. Create appointment 2 at the exact same time slot -> Should succeed now
    resp2 = client.post(
        "/appointments/",
        json={"patient_id": pat2_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": slot_iso},
        headers=headers,
    )
    assert resp2.status_code == 201
    assert resp2.json()["status"] == "scheduled"