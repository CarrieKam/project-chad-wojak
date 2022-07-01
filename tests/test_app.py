import unittest
import os
os.environ['TESTING'] = 'true'
from tests import test_db


from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Personal Portfolio</title>" in html
        assert "<p>&#169 Copyright chad-wojak. 2022 All rights reserved</p>" in html

    def test_timeline(self):
        response1 = self.client.get("/api/timeline_post")
        assert response1.status_code == 200
        assert response1.is_json
        json = response1.get_json()
        assert "timeline_posts" in json
        # list should contain 0 elements
        assert len(response1.get_json(["timeline_posts"])) == 1

        # using the db test, post 2 documents to the db, request them back, and re-assert
        test_db.TestTimelinePost.test_timeline_post(self)
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 2



    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "helloworld"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post("/api/timeline_post", data={"name": "john", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post("/api/timeline_post", data={"name": "john", "email": "not-an-email", "content": "hello"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
