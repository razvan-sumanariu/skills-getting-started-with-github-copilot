from src.app import activities as activity_store


def test_get_activities(api_client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = api_client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert activity_name in response.json()
    assert isinstance(response.json()[activity_name]["participants"], list)


def test_signup_for_activity(api_client):
    # Arrange
    activity_name = "Basketball Team"
    email = "new.student@example.com"

    # Act
    response = api_client.post(
        f"/activities/{activity_name.replace(' ', '%20')}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    activities = api_client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(api_client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = api_client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    activities = api_client.get("/activities").json()
    assert activities[activity_name]["participants"].count(email) == 1


def test_signup_rejects_unknown_activity(api_client):
    # Arrange
    email = "new.student@example.com"

    # Act
    response = api_client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant(api_client):
    # Arrange
    activity_name = "Basketball Team"
    email = "student@example.com"
    activity_store[activity_name]["participants"].append(email)

    # Act
    response = api_client.delete(
        "/activities/Basketball%20Team/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    activities = api_client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_rejects_unregistered_participant(api_client):
    # Arrange
    email = "not.registered@example.com"

    # Act
    response = api_client.delete(
        "/activities/Basketball%20Team/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_rejects_unknown_activity(api_client):
    # Arrange
    email = "student@example.com"

    # Act
    response = api_client.delete(
        "/activities/Unknown%20Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"