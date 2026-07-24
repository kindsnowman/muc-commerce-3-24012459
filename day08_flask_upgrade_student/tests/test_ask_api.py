def test_ask_empty_question_returns_400(client):
    resp = client.post("/api/ask", json={"question": ""})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["ok"] is False
    assert "answer" in data

def test_ask_missing_question_field_returns_400(client):
    resp = client.post("/api/ask", json={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["ok"] is False