def test_metrics_returns_ok_and_four_items(client):
    resp = client.get("/api/metrics")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert len(data["metrics"]) == 4

def test_metrics_each_item_has_required_keys(client):
    resp = client.get("/api/metrics")
    data = resp.get_json()
    for item in data["metrics"]:
        assert "label" in item
        assert "value" in item
        assert "note" in item