# test_db.py

import unittest
from peewee import *

from app import TimelinePost
from playhouse.shortcuts import model_to_dict


MODELS = [TimelinePost]

#use an in-memeory SQLite for tests
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_post(self):
        
       # Create 2 timeline posts:
        first_post = TimelinePost.create(
            name="Sam", email="sam@gmail.com", content="Hello, world!"
        )
        assert first_post.id == 1

        second_post = TimelinePost.create(
            name="Tyler", email="tyler@gmail.com", content="Hello, world, again!"
        )
        assert second_post.id == 2

        # now that we know both posts have id 1 and 2, request them and assert that they are correct
        response1 = model_to_dict(TimelinePost.get_by_id(1))
        response2 = model_to_dict(TimelinePost.get_by_id(2))

        assert first_post.name == response1["name"]
        assert first_post.email == response1["email"]
        assert first_post.content == response1["content"]
        assert first_post.created_at == response1["created_at"]

        assert second_post.name == response2["name"]
        assert second_post.email == response2["email"]
        assert second_post.content == response2["content"]
        assert second_post.created_at == response2["created_at"]

        
