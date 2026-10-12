import uuid
import hashlib
import platform


def get_machine_id() -> str:
    raw = (
        str(uuid.getnode()) +
        platform.node() +
        platform.machine() +
        platform.processor() +
        platform.system()
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
