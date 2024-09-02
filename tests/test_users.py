import pytest
from sqlalchemy import insert, select


# from conftest import client, async_session_maker



def test_one():
    assert 1 == 1

# def test_create_users():
#     response = client.post("/api/users", json={
#         "username": "string19",
#         "email": "user19@example.com",
#         "password": "string19",
#     })
#
#     assert response.status_code == 201