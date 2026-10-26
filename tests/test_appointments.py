from datetime import datetime, timezone


def test_create_and_get_appointment(client):
    #  Register and Login
    user_data = {"username": "apptadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    #  Create Doctor
    doc_resp = client.post(
        "/doctors/",
        json={"name": "Dr. Maria Dan", "specialization": "Neurologie", "phone": "0733445566"},
        headers=headers,
    )
    doctor_id = doc_resp.json()["id"]

    #  Create Patient
    pat_resp = client.post(
        "/patients/",
        json={"name": "Ana Radu", "age": 30, "disease": "Migrena", "doctor_id": doctor_id},
        headers=headers,
    )
    patient_id = pat_resp.json()["id"]

    #  Create Medical Service
    srv_resp = client.post(
        "/services/",
        json={"name": "Consultatie Neurologie", "price": 200.0, "duration_minutes": 30},
        headers=headers,
    )
    service_id = srv_resp.json()["id"]

    #  Create Appointment
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

    # 6. Retrieve All Appointments
    get_all = client.get("/appointments/")
    assert get_all.status_code == 200
    assert len(get_all.json()) == 1

    # 7. Retrieve One Appointment
    get_one = client.get(f"/appointments/{appt_id}")
    assert get_one.status_code == 200
    assert get_one.json()["id"] == appt_id


def test_delete_appointment(client):
    #  Register and Login
    user_data = {"username": "apptadmin2", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    #  Create Prerequisites
    doc_id = client.post("/doctors/", json={"name": "Dr. Pop", "specialization": "ORL", "phone": "0700"}, headers=headers).json()["id"]
    pat_id = client.post("/patients/", json={"name": "Ion", "age": 20, "disease": "Rinită", "doctor_id": doc_id}, headers=headers).json()["id"]
    srv_id = client.post("/services/", json={"name": "Consult", "price": 100.0, "duration_minutes": 15}, headers=headers).json()["id"]

    #  Create Appointment
    now_iso = datetime.now(timezone.utc).isoformat()
    appt = client.post("/appointments/", json={"patient_id": pat_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": now_iso}, headers=headers).json()

    #  Delete Appointment
    del_resp = client.delete(f"/appointments/{appt['id']}", headers=headers)
    assert del_resp.status_code == 200

    #  Verify deletion
    get_resp = client.get(f"/appointments/{appt['id']}")
    assert get_resp.status_code == 404


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
    assert respstatus_code == 201

    # Try Overlapping Appointment (10:15 - 10:45) -> Should Fail with HTTP 400
    overlap_iso = "2026-11-01T10:15:00"
    resp2 = client.post(
        "/appointments/",
        json={"patient_id": pat2_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": overlap_iso},
        headers=headers,
    )
    assert respstatus_code == 400
    assert "not available" in respjson()["detail"].lower()


def test_update_appointment_status(client):
    # Register and Login
    user_data = {"username": "statusadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Setup Prerequisites
    doc_id = client.post("/doctors/", json={"name": "Dr. Status", "specialization": "Dermatologie", "phone": "0711"}, headers=headers).json()["id"]
    pat_id = client.post("/patients/", json={"name": "Maria", "age": 25, "disease": "Acnee", "doctor_id": doc_id}, headers=headers).json()["id"]
    srv_id = client.post("/services/", json={"name": "Consult", "price": 120.0, "duration_minutes": 20}, headers=headers).json()["id"]

    now_iso = "2026-12-01T14:00:00"
    appt = client.post("/appointments/", json={"patient_id": pat_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": now_iso}, headers=headers).json()

    # Update status to 'completed'
    update_resp = client.patch(f"/appointments/{appt['id']}/status", json={"status": "completed"}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "completed"

    # Try updating to an invalid status -> Should return HTTP 400
    invalid_resp = client.patch(f"/appointments/{appt['id']}/status", json={"status": "invalid_status"}, headers=headers)
    assert invalid_resp.status_code == 400


def test_cancelled_appointment_frees_slot(client):
    # Register and Login
    user_data = {"username": "freeslotadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Setup Prerequisites
    doc_id = client.post("/doctors/", json={"name": "Dr. Free", "specialization": "Pediatrie", "phone": "0722"}, headers=headers).json()["id"]
    pat1_id = client.post("/patients/", json={"name": "Copil 1", "age": 5, "disease": "Gripa", "doctor_id": doc_id}, headers=headers).json()["id"]
    pat2_id = client.post("/patients/", json={"name": "Copil 2", "age": 8, "disease": "Tuse", "doctor_id": doc_id}, headers=headers).json()["id"]
    srv_id = client.post("/services/", json={"name": "Consult", "price": 100.0, "duration_minutes": 30}, headers=headers).json()["id"]

    slot_iso = "2026-12-10T09:00:00"

    # Create appointment 1
    appt1 = client.post("/appointments/", json={"patient_id": pat1_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": slot_iso}, headers=headers).json()

    # Cancel appointment 1
    client.patch(f"/appointments/{appt1['id']}/status", json={"status": "cancelled"}, headers=headers)

    # Create appointment 2 at the exact same time slot -> Should succeed now
    resp2 = client.post("/appointments/", json={"patient_id": pat2_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": slot_iso}, headers=headers)
    assert respstatus_code == 201
    assert respjson()["status"] == "scheduled"