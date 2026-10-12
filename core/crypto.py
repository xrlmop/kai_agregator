import os
import json
import hashlib
import base64
from pathlib import Path

from cryptography.fernet import Fernet


CONFIG_DIR = Path.home() / ".kai_aggregator"
ROOT_FILE = CONFIG_DIR / "root.json"
MASTER_FILE = CONFIG_DIR / "master.enc"

PBKDF2_ITERATIONS = 200_000
PBKDF2_ALGO = "sha256"
KEY_LEN = 32


def ensure_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def derive_keys(password: str, salt: bytes):
    dk = hashlib.pbkdf2_hmac(
        PBKDF2_ALGO, password.encode("utf-8"), salt,
        PBKDF2_ITERATIONS, dklen=KEY_LEN * 2,
    )
    return dk[:KEY_LEN], dk[KEY_LEN:]


def hash_verify_key(verify_key: bytes) -> str:
    return hashlib.sha256(verify_key).hexdigest()


def fernet_from_key(encrypt_key: bytes) -> Fernet:
    return Fernet(base64.urlsafe_b64encode(encrypt_key))


def load_root():
    if not ROOT_FILE.exists():
        return None
    with open(ROOT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_root(data: dict):
    ensure_dir()
    with open(ROOT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def is_root_configured() -> bool:
    return ROOT_FILE.exists()


def create_root(password: str, username: str = "root") -> dict:
    ensure_dir()
    salt = os.urandom(16)
    verify_key, _ = derive_keys(password, salt)
    verify_hash = hash_verify_key(verify_key)

    root_secret = base64.urlsafe_b64encode(os.urandom(32)).decode()

    owner = {
        "username": username,
        "salt": base64.b64encode(salt).decode(),
        "verify_hash": verify_hash,
        "role": "owner",
        "created": int(__import__("time").time()),
    }

    data = {
        "version": 2,
        "root_secret": root_secret,
        "licenses": [],
        "admins": [owner],
    }
    save_root(data)
    return data


def verify_root_password(password: str):
    data = load_root()
    if not data:
        return False, None
    for a in data.get("admins", []):
        if a.get("role") != "owner":
            continue
        salt = base64.b64decode(a["salt"])
        verify_key, encrypt_key = derive_keys(password, salt)
        if hash_verify_key(verify_key) == a["verify_hash"]:
            return True, encrypt_key
    return False, None
    salt = base64.b64decode(data["salt"])
    verify_key, encrypt_key = derive_keys(password, salt)
    if hash_verify_key(verify_key) == data["verify_hash"]:
        return True, encrypt_key
    return False, None


def encrypt_master_key(encrypt_key: bytes, plaintext: str):
    ensure_dir()
    f = fernet_from_key(encrypt_key)
    token = f.encrypt(plaintext.encode("utf-8"))
    with open(MASTER_FILE, "wb") as fp:
        fp.write(token)


def decrypt_master_key(encrypt_key: bytes):
    if not MASTER_FILE.exists():
        return None
    f = fernet_from_key(encrypt_key)
    try:
        with open(MASTER_FILE, "rb") as fp:
            return f.decrypt(fp.read()).decode("utf-8")
    except Exception:
        return None


def has_master_key() -> bool:
    return MASTER_FILE.exists()


def delete_master_key():
    if MASTER_FILE.exists():
        MASTER_FILE.unlink()
