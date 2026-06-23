from src.app import activities


def test_unregister_removes_existing_participant(client):
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/Chess Club/participants?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_rejects_unknown_activity(client):
    response = client.delete("/activities/Unknown Club/participants?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_missing_participant(client):
    response = client.delete(
        "/activities/Chess Club/participants?email=notregistered@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_then_signup_same_student(client):
    email = "michael@mergington.edu"

    unregister_response = client.delete(f"/activities/Chess Club/participants?email={email}")
    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
    assert email in activities["Chess Club"]["participants"]
