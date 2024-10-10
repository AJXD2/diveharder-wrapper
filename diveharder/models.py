from pydantic import BaseModel


class APIURLConfiguration(BaseModel):
    diveharder: str
    community: str
