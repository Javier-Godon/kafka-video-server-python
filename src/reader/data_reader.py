import base64

import uuid6

from definitions import ROOT_DIR
from src.reader.video_data import VideoData
from src.videoproducer import video_producer


async def read_file_by_chunks(sha_id: str, element_id: str, element_alias: str, unix_epoch_start: int,
                              unix_epoch_end: int, video_path: str):
    uuid = str(uuid6.uuid7())
    buffer = 400_000
    chunk = 0
    file = open(f'{ROOT_DIR}/{video_path}', "rb")
    read = file.read(buffer)
    while read:
        encoded_base64 = base64.b64encode(read)
        video_producer(VideoData(uuid=uuid, sha_id=sha_id, element_id=element_id, element_alias=element_alias,
                                 unix_epoch_start=unix_epoch_start, unix_epoch_end=unix_epoch_end, chunk_index=chunk,
                                 data=encoded_base64.decode()))

        read = file.read(buffer)

        chunk += 1
