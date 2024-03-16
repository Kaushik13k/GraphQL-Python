import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from app.services.signup import (
    SignUp,
    SignupDataException,
    hash_password,
    execute_query,
)


class TestSignup:
    @pytest.fixture
    def setup(self):
        self.user_input = {
            "first_name": "Test",
            "last_name": "User",
            "user_name": "testuser",
            "email": "testuser@example.com",
            "password": "password",
            "phone_number": 1234567890,
            "age": 30,
        }

    @patch("app.services.signup.hash_password")
    @patch("app.services.signup.execute_query")
    def test_signup_success(self, mock_execute_query, mock_hash_password, setup):
        mock_hash_password.return_value = ("salt", "hashed_password")
        mock_execute_query.return_value = None

        result = SignUp.mutate(None, None, self.user_input)

        assert result.username == self.user_input["user_name"]
        assert result.email == self.user_input["email"]

    @patch("app.services.signup.hash_password")
    @patch("app.services.signup.execute_query")
    def test_signup_db_error(self, mock_execute_query, mock_hash_password, setup):
        mock_hash_password.return_value = ("salt", "hashed_password")
        mock_execute_query.side_effect = SQLAlchemyError

        with pytest.raises(SignupDataException):
            SignUp.mutate(None, None, self.user_input)

    def test_hash_password(self, setup):
        salt, hashed_password = hash_password(self.user_input["password"])

        assert salt is not None
        assert hashed_password is not None

    @patch("app.services.signup.Session")
    def test_execute_query_success(self, mock_session, setup):
        mock_session.return_value.__enter__.return_value.execute.return_value = (
            MagicMock(returns_rows=False)
        )

        result = execute_query("SELECT * FROM users")

        assert result is None

    @patch("app.services.signup.Session")
    def test_execute_query_error(self, mock_session, setup):
        mock_session.return_value.__enter__.return_value.execute.side_effect = (
            SQLAlchemyError
        )

        with pytest.raises(SQLAlchemyError):
            execute_query("SELECT * FROM users")
