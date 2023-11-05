from definitions import ROOT_DIR
from src.reader.video_data import VideoData
from src.videoproducer import video_producer


def read_file_by_chunks(sha_id: str, element_id: str, element_alias: str, unix_epoch: int):
    buffer = 400000
    chunk = 0
    file = open(f'{ROOT_DIR}/resources/80MbSample.webm', "rb")

    read = file.read(buffer)
    while read:
        video_producer(VideoData(sha_id=sha_id, element_id=element_id, element_alias=element_alias,
                                 unix_epoch=unix_epoch, chunk_index=chunk, data=str(read)))

        read = file.read(buffer)

        chunk += 1
