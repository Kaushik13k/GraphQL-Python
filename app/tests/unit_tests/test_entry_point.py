# FILEPATH: /Users/kaushikk/Desktop/BACKEND-MyGymApp/tests/unit_tests/test_entry_point.py

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.entry_point import entry_point

# from services.mutation import Mutation
# from services.query import Query
import graphene

app = FastAPI()
app.post("/entry_point")(entry_point)
client = TestClient(app)


def test_entry_point_success():
    request = {"operation_name": "test", "query": "query { test }", "variables": {}}
    response = client.post("/entry_point", json=request)
    assert response.status_code == 200
    assert "data" in response.json()


def test_entry_point_failure():
    request = {
        "operation_name": "test",
        "query": "query { non_existent_query }",
        "variables": {},
    }
    response = client.post("/entry_point", json=request)
    assert response.status_code == 400
    assert "error" in response.json()


def test_entry_point_no_operation_name():
    request = {"query": "query { test }", "variables": {}}
    response = client.post("/entry_point", json=request)
    assert response.status_code == 400
    assert "error" in response.json()
