from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class VideoDataRequest(BaseModel):
    sha_id: str
    element_id: str
    element_alias: str
    unix_epoch_start: int
    unix_epoch_end: int
    video_path: str
