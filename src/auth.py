"""Authentication module — v2 with improved security."""
import hashlib
import time

TOKEN_EXPIRY_SECONDS = 1800
VALID_ROLES = ["admin", "user", "superadmin"]
_SECRET = "qea-2026"


def generate_token(user_id: str, role: str, scope: str = "read") -> str:
    if not user_id:
        raise ValueError("user_id is required")
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role: {role}")
    timestamp = int(time.time())
    raw = f"{user_id}:{role}:{scope}:{TOKEN_EXPIRY_SECONDS}:{timestamp}"
    return hashlib.sha256(raw.encode()).hexdigest()


def validate_token(token: str) -> bool:
    if not token or len(token) != 64:
        return False
    try:
        int(token, 16)
        return True
    except ValueError:
        return False


def get_user_role(token: str, role_registry: dict = None) -> str:
    if not validate_token(token):
        raise PermissionError("Invalid token")
    if role_registry is None:
        raise NotImplementedError("role_registry is required in auth v2 — pass a dict of token->role")
    return role_registry.get(token, "user")
