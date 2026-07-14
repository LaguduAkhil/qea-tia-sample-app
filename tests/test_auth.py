"""Tests for auth module."""

import pytest
from src.auth import generate_token, validate_token, get_user_role


def test_generate_token_success():
    token = generate_token("user123", "admin")
    assert isinstance(token, str)
    assert len(token) == 64


def test_generate_token_invalid_role():
    with pytest.raises(ValueError, match="Invalid role"):
        generate_token("user123", "superuser")


def test_generate_token_empty_user():
    with pytest.raises(ValueError, match="user_id is required"):
        generate_token("", "user")


def test_validate_token_valid():
    token = generate_token("user123", "user")
    assert validate_token(token) is True


def test_validate_token_short():
    assert validate_token("abc") is False


def test_validate_token_empty():
    assert validate_token("") is False


def test_get_user_role_valid():
    token = generate_token("user123", "user")
    role = get_user_role(token)
    assert role == "user"


def test_get_user_role_invalid_token():
    with pytest.raises(PermissionError, match="Invalid token"):
        get_user_role("bad")
