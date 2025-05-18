from datetime import datetime, UTC
from pydantic import BaseModel


def get_timestamp():
    return datetime.now(UTC).isoformat()


def model_dump_without_none_values(payload: BaseModel):
    model_dump = payload.model_dump()
    return {key: value for key, value in model_dump.items() if value is not None}
