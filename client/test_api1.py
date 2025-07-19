import requests
import pytest

BASE_URL = "http://localhost:8001"

@pytest.mark.skip(reason="todo")
def test_health():
    resp = requests.get(f"{BASE_URL}/health")
    print("Health:", resp.status_code, resp.json())

@pytest.mark.skip(reason="todo")
def test_quiz(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/api/v1/quiz", headers=headers)
    print("Quiz:", resp.status_code, resp.json())

if __name__ == "__main__":
    test_health()
    # Replace with a valid token if needed
    test_quiz(token="your_token_here")
