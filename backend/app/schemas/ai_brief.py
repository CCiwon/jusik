from pydantic import BaseModel


class OpeningBriefResponse(BaseModel):
    sentences: list[str]
    content: str
    generated_at: str
    snapshot_hash: str
    cached: bool
