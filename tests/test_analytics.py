def test_analytics_endpoints(client):
    # Register and Login
    user_data = {"username": "analyticsadmin", "password": "pass1234password"}
    client.post("/auth/register", json=user_data)
    login_resp = client.post("/auth/login", data=user_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Prerequisites
    doc_id = client.post(
        "/doctors/",
        json={"name": "Dr. Analytics", "specialization": "Cardiologie", "phone": "0733"},
        headers=headers,
    ).json()["id"]

    pat_id = client.post(
        "/patients/",
        json={"name": "Ionut Analytics", "age": 35, "disease": "None", "doctor_id": doc_id},
        headers=headers,
    ).json()["id"]

    srv_id = client.post(
        "/services/",
        json={"name": "EKG", "price": 150.0, "duration_minutes": 20},
        headers=headers,
    ).json()["id"]

    # Create Appointment and complete it
    appt_id = client.post(
        "/appointments/",
        json={"patient_id": pat_id, "doctor_id": doc_id, "service_id": srv_id, "appointment_date": "2026-12-20T10:00:00"},
        headers=headers,
    ).json()["id"]

    client.patch(f"/appointments/{appt_id}/status", json={"status": "completed"}, headers=headers)

    # Test Summary Endpoint
    summary_resp = client.get("/analytics/summary", headers=headers)
    assert summary_resp.status_code == 200
    summary_data = summary_resp.json()
    assert summary_data["total_active_patients"] == 1
    assert summary_data["total_doctors"] == 1
    assert summary_data["completed_appointments"] == 1
    assert summary_data["total_revenue"] == 150.0

    # Test Doctor Analytics Endpoint
    doc_analytics = client.get("/analytics/doctors", headers=headers)
    assert doc_analytics.status_code == 200
    assert len(doc_analytics.json()) == 1
    assert doc_analytics.json()[0]["total_revenue"] == 150.0

    # Test Services Analytics Endpoint
    srv_analytics = client.get("/analytics/services", headers=headers)
    assert srv_analytics.status_code == 200
    assert len(srv_analytics.json()) == 1
    assert srv_analytics.json()[0]["total_revenue"] == 150.0