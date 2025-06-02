import uuid
from typing import Union

def uuid_to_bytes(uuid_val: Union[str, uuid.UUID, bytes]) -> bytes:
    if isinstance(uuid_val, bytes):
        return uuid_val
    elif isinstance(uuid_val, str):
        return uuid.UUID(uuid_val).bytes
    elif isinstance(uuid_val, uuid.UUID):
        return uuid_val.bytes
    else:
        raise ValueError(f"Tipo UUID inválido: {type(uuid_val)}")

def bytes_to_uuid_str(uuid_bytes: bytes) -> str:
    if isinstance(uuid_bytes, str):
        return uuid_bytes
    return str(uuid.UUID(bytes=uuid_bytes))

def generate_uuid_str() -> str:
    return str(uuid.uuid4())

def generate_uuid_bytes() -> bytes:
    return uuid.uuid4().bytes