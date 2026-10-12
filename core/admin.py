import os
import time
import base64
import hashlib

from core.crypto import (
    derive_keys, hash_verify_key, load_root, save_root,
)


def _make_admin_record(username: str, password: str, role: str = "moderator") -> dict:
    salt = os.urandom(16)
    verify_key, _ = derive_keys(password, salt)
    return {
        "username": username,
        "salt": base64.b64encode(salt).decode(),
        "verify_hash": hash_verify_key(verify_key),
        "role": role,
        "created": int(time.time()),
    }


def add_admin(username: str, password: str, role: str = "moderator") -> bool:
    data = load_root()
    if not data:
        return False
    admins = data.setdefault("admins", [])
    if any(a["username"] == username for a in admins):
        return False
    admins.append(_make_admin_record(username, password, role))
    save_root(data)
    return True


def verify_admin(username: str, password: str):
    data = load_root()
    if not data:
        return None, None
    admins = data.get("admins", [])
    for a in admins:
        if a["username"] != username:
            continue
        salt = base64.b64decode(a["salt"])
        verify_key, encrypt_key = derive_keys(password, salt)
        if hash_verify_key(verify_key) == a["verify_hash"]:
            return a["role"], encrypt_key
        return None, None
    return None, None


def list_admins() -> list:
    data = load_root()
    if not data:
        return []
    return data.get("admins", [])


def delete_admin(username: str) -> bool:
    data = load_root()
    if not data:
        return False
    admins = data.get("admins", [])
    before = len(admins)
    data["admins"] = [a for a in admins if a["username"] != username]
    if len(data["admins"]) != before:
        save_root(data)
        return True
    return False
