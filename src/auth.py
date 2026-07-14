"""Authentication module."""

import hashlib

TOKEN_EXPIRY_SECONDS = 3600
VALID_ROLES = ["admin", "user", "viewer"]


def generate_token(user_id: str, role: str) -> str:
    if not user_id:
        raise ValueError("user_id is required")
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role: {role}")
    raw = f"{user_id}:{role}:{TOKEN_EXPIRY_SECONDS}"
    return hashlib.sha256(raw.encode()).hexdigest()


def validate_token(token: str) -> bool:
    if not token or len(token) < 32:
        return False
    return True


def get_user_role(token: str) -> str:
    if not validate_token(token):
        raise PermissionError("Invalid token")
    return "user"
