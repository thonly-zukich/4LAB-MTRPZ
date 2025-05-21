# tests/test_api.py
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Привіт, котики!"

def test_random_cat(client, monkeypatch):
    def mock_catapi(url):
        class MockResponse:
            def json(self):
                return [{"url": "http://cat.com/cat.jpg"}]
        return MockResponse()
    
    def mock_factapi(url):
        class MockResponse:
            def json(self):
                return {"fact": "Cats purr."}
        return MockResponse()

    monkeypatch.setattr("httpx.get", lambda url: mock_catapi(url) if "thecatapi" in url else mock_factapi(url))

    response = client.get("/random_cat")
    assert response.status_code == 200
    data = response.json()
    assert "image_url" in data
    assert "fact" in data

def test_vote_and_top(client):
    vote_data = {
        "image_url": "http://cat.com/cat.jpg",
        "fact": "Cats purr."
    }
    vote_response = client.post("/vote", json=vote_data)
    assert vote_response.status_code == 200

    top_response = client.get("/top")
    assert top_response.status_code == 200
    assert isinstance(top_response.json(), list)
    assert top_response.json()[0]["image_url"] == vote_data["image_url"]

def test_clear_votes(client):
    response = client.post("/clear_votes")
    assert response.status_code == 200
    assert "Всі голоси видалено" in response.json()["message"]
