def test_categories_no_param_returns_all(client):
    resp = client.get("/api/categories")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["ok"] is True
    assert data["category"] == "全部"
    assert isinstance(data["rows"], list)

def test_categories_with_filter_returns_matching(client):
    resp = client.get("/api/categories?category=Fashion")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["ok"] is True
    assert data["category"] == "Fashion"
    assert isinstance(data["rows"], list)