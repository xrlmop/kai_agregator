import time
import hmac
import hashlib
import secrets
import json
from pathlib import Path

from core.crypto import load_root, save_root
from core.machine import get_machine_id


LICENSE_FILE = Path.home() / ".kai_aggregator" / "license.json"


def _sign(payload: str, secret: str) -> str:
    return hmac.new(
        secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()[:16]


def generate_license(owner: str, days: int = 30, machine_id: str = "") -> dict:
    data = load_root()
    if not data:
        raise RuntimeError("Root не настроен")

    secret = data["root_secret"]
    created = int(time.time())
    nonce = secrets.token_hex(4)
    payload = f"{created}:{days}:{nonce}"
    signature = _sign(payload, secret)
    key = f"{payload}:{signature}"

    entry = {
        "key": key,
        "owner": owner,
        "created": created,
        "days": days,
        "active": True,
        "machine_id": machine_id or "",
    }
    data["licenses"].append(entry)
    save_root(data)
    return entry


def validate_license(key: str) -> dict:
    data = load_root()
    if not data:
        return {"valid": False, "reason": "root не настроен"}

    secret = data["root_secret"]

    try:
        payload, signature = key.rsplit(":", 1)
        expected = _sign(payload, secret)
        if not hmac.compare_digest(signature, expected):
            return {"valid": False, "reason": "подпись неверна"}

        created_s, days_s, _nonce = payload.split(":")
        created = int(created_s)
        days = int(days_s)

        if days == 0:
            expires = 0
        else:
            expires = created + days * 86400
            if time.time() > expires:
                return {"valid": False, "reason": "лицензия истекла"}

        for entry in data["licenses"]:
            if entry["key"] != key:
                continue

            if not entry.get("active", True):
                return {"valid": False, "reason": "лицензия отозвана"}

            bound_machine = entry.get("machine_id", "")
            if bound_machine:
                current = get_machine_id()
                if current != bound_machine:
                    return {
                        "valid": False,
                        "reason": "лицензия привязана к другому устройству",
                    }

            return {
                "valid": True,
                "created": created,
                "days": days,
                "expires": expires,
                "owner": entry.get("owner", ""),
            }

        return {"valid": False, "reason": "лицензия не найдена в базе"}
    except Exception as e:
        return {"valid": False, "reason": f"ошибка: {e}"}


def list_licenses() -> list:
    data = load_root()
    if not data:
        return []
    return data["licenses"]


def revoke_license(key: str) -> bool:
    data = load_root()
    if not data:
        return False
    for entry in data["licenses"]:
        if entry["key"] == key:
            entry["active"] = False
            save_root(data)
            return True
    return False


def delete_license(key: str) -> bool:
    data = load_root()
    if not data:
        return False
    before = len(data["licenses"])
    data["licenses"] = [l for l in data["licenses"] if l["key"] != key]
    if len(data["licenses"]) != before:
        save_root(data)
        return True
    return False


def save_user_license(key: str):
    LICENSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LICENSE_FILE, "w", encoding="utf-8") as f:
        json.dump({"key": key, "machine_id": get_machine_id()}, f, indent=2)


def load_user_license():
    if not LICENSE_FILE.exists():
        return None
    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("machine_id") != get_machine_id():
            return None
        return data.get("key")
    except Exception:
        return None


def clear_user_license():
    if LICENSE_FILE.exists():
        LICENSE_FILE.unlink()


def has_valid_user_license() -> dict:
    key = load_user_license()
    if not key:
        return {"valid": False, "reason": "лицензия не активирована"}
    return validate_license(key)
