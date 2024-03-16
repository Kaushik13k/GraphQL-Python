# import pytest
# from fastapi import FastAPI
# from fastapi.testclient import TestClient
# from app.main import lifespan


# @pytest.mark.asyncio
# async def test_lifespan():
#     app = FastAPI()

#     async with lifespan(app):

#         @app.get("/")
#         def health():
#             return {"Status": "Running"}

#         client = TestClient(app)
#         response = client.get("/")
#         print(response.status_code)
#         assert response.status_code == 200
