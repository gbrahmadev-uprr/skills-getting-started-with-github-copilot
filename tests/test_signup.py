from src.app import activities


def test_signup_successfully_registers_new_student(client):
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_student(client):
    email = "michael@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_unknown_activity(client):
    response = client.post("/activities/Unknown Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_when_activity_is_full(client):
    activity = activities["Chess Club"]
    activity["participants"] = [
        f"student{i}@mergington.edu" for i in range(activity["max_participants"])
    ]

    response = client.post("/activities/Chess Club/signup?email=overflow@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_signup_requires_email_query_parameter(client):
    response = client.post("/activities/Chess Club/signup")

    assert response.status_code == 422


def test_signup_does_not_modify_other_activities(client):
    email = "isolated@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]
    assert email not in activities["Programming Class"]["participants"]
