"""
Complex auth tests — structural and behavioral assertions that break
when token format, role set, or validation logic changes.
"""
import pytest
from src.auth import (
    generate_token,
    validate_token,
    get_user_role,
    VALID_ROLES,
    TOKEN_EXPIRY_SECONDS,
)


def test_valid_roles_exact_set():
    """VALID_ROLES must be exactly this set — fails when any role is added or removed."""
    assert set(VALID_ROLES) == {"admin", "user", "viewer"}


def test_token_expiry_is_3600():
    """TOKEN_EXPIRY_SECONDS must be 3600 (one hour)."""
    assert TOKEN_EXPIRY_SECONDS == 3600


def test_generate_token_is_deterministic():
    """Same inputs must always produce the same token — breaks if timestamp is added."""
    token_a = generate_token("user99", "admin")
    token_b = generate_token("user99", "admin")
    assert token_a == token_b, f"Token is non-deterministic: {token_a} != {token_b}"


def test_validate_token_accepts_non_hex_string():
    """Current validator accepts any string >= 10 chars including non-hex."""
    assert validate_token("x" * 10) is True
    assert validate_token("hello-world-123") is True


def test_get_user_role_no_registry_needed():
    """get_user_role() works with only a token — no second argument needed."""
    token = generate_token("user1", "admin")
    role = get_user_role(token)
    assert role == "user"


def test_viewer_role_generates_token():
    """viewer is a valid role — fails if removed from VALID_ROLES."""
    token = generate_token("viewer_user", "viewer")
    assert len(token) == 64
    assert validate_token(token) is True


def test_all_current_roles_produce_64char_tokens():
    """Every current valid role generates a 64-char hex token."""
    for role in VALID_ROLES:
        token = generate_token(f"u_{role}", role)
        assert len(token) == 64, f"Token for role '{role}' has wrong length"
        assert isinstance(token, str)
