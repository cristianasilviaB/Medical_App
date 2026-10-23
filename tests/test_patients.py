def test_soft_delete_patient(client):
    # 1. Inregistrare si Login
    user_data = {"username": "patientadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create doctor to associate with the patient
    doc_resp = client.post(
        "/doctors/",
        json={"name": "Dr. Smith", "specialization": "Cardiologie", "phone": "0711223344"},
        headers=headers,
    )
    doctor_id = doc_resp.json()["id"]

    # Create a patient
    pat_resp = client.post(
        "/patients/",
        json={"name": "Ion Popescu", "age": 45, "disease": "Gripa", "doctor_id": doctor_id},
        headers=headers,
    )
    assert pat_resp.status_code == 201
    patient_id = pat_resp.json()["id"]
    assert pat_resp.json()["is_deleted"] is False

    # Soft Delete Pacient
    del_resp = client.delete(f"/patients/{patient_id}", headers=headers)
    assert del_resp.status_code == 200

    # verify that the patient is soft-deleted
    get_all_resp = client.get("/patients/")
    assert get_all_resp.status_code == 200
    assert len(get_all_resp.json()) == 0

    # VERIFY that the patient is not returned in the GET /patients/{id} endpoint
    get_one_resp = client.get(f"/patients/{patient_id}")
    assert get_one_resp.status_code == 404