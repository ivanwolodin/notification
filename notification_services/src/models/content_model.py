import orjson
from pydantic import BaseModel


class BaseContent(BaseModel):

    user_id: str
    event_type: str

    class Config:
        json_loads = orjson.loads
