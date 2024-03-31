import orjson
from pydantic import BaseModel


class BaseContent(BaseModel):

    user_id: str
    event_type: str
    subject: str
    body: str

    class Config:
        json_loads = orjson.loads
