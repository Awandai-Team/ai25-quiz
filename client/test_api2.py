import requests

BASE_URL = "http://localhost:8000"

def test_health():
    resp = requests.get(f"{BASE_URL}/health")
    print("Health:", resp.status_code, resp.json())

def test_submit_answer(question_id, answer):
    payload = {
        "question_id": question_id,
        "answer": answer
    }
    resp = requests.post(f"{BASE_URL}/api/v1/answer", json=payload)
    print("Submit Answer:", resp.status_code, resp.json())

if __name__ == "__main__":
    test_health()
    # Example usage; replace with actual values as needed
    test_submit_answer(question_id=123, answer="B")