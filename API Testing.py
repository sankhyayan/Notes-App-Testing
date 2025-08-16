import requests
import json
import random
import string

BASE_URL = "https://practice.expandtesting.com/notes/api"

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def test_register_user():
    email = f"{generate_random_string()}@example.com"
    password = "password123"
    name = "Test User"
    payload = {
        "name": name,
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/users/register", json=payload)
    assert response.status_code == 201, f"Registration failed: {response.text}"
    data = response.json()
    assert "data" in data, "No data in response"
    assert data["data"]["email"] == email, "Email mismatch"
    return email, password

def test_login_user(email, password):
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/users/login", json=payload)
    assert response.status_code == 200, f"Login failed: {response.text}"
    data = response.json()
    assert "data" in data, "No data in response"
    assert "token" in data["data"], "No token in response"
    print("completed")
    print("completed")
    return data["data"]["token"]

def test_create_note(token):
    headers = {"x-auth-token": token}
    payload = {
        "title": "Test Note",
        "description": "This is a test note",
        "category": "Home"
    }
    response = requests.post(f"{BASE_URL}/notes", json=payload, headers=headers)
    assert response.status_code == 200, f"Note creation failed: {response.text}"
    data = response.json()
    assert "data" in data, "No data in response"
    assert data["data"]["title"] == "Test Note", "Title mismatch"
    print("completed")
    return data["data"]["id"]

def test_get_notes(token):
    headers = {"x-auth-token": token}
    response = requests.get(f"{BASE_URL}/notes", headers=headers)
    assert response.status_code == 200, f"Get notes failed: {response.text}"
    data = response.json()
    assert "data" in data, "No data in response"
    print("completed")
    return data["data"]

def test_update_note(token, note_id):
    headers = {"x-auth-token": token}
    payload = {
        "title": "Updated Test Note",
        "description": "This is an updated test note",
        "category": "Work",
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=payload, headers=headers)
    assert response.status_code == 200, f"Note update failed: {response.text}"
    data = response.json()
    assert "data" in data, "No data in response"
    assert data["data"]["title"] == "Updated Test Note", "Title mismatch"
    assert data["data"]["completed"] == True, "Completed status mismatch"
    print("completed")

def test_delete_note(token, note_id):
    headers = {"x-auth-token": token}
    response = requests.delete(f"{BASE_URL}/notes/{note_id}", headers=headers)
    assert response.status_code == 200, f"Note deletion failed: {response.text}"
    data = response.json()
    assert "message" in data, "No message in response"
    assert data["message"] == "Note successfully deleted", "Deletion message mismatch"
    print("completed")

def main():
    email, password = test_register_user()
    token = test_login_user(email, password)
    note_id = test_create_note(token)
    notes = test_get_notes(token)
    assert any(note["id"] == note_id for note in notes), "Created note not found"
    test_update_note(token, note_id)
    test_delete_note(token, note_id)
    notes_after_delete = test_get_notes(token)
    assert not any(note["id"] == note_id for note in notes_after_delete), "Deleted note still present"
    print("completed")

if __name__ == "__main__":
    main()
