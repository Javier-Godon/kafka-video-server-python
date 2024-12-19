import base64
import dataclasses
import json
import time
from datetime import datetime

import uuid6
from kafka import KafkaProducer

from app.configuration.configuration import get_data
from definitions import ROOT_DIR
from app.file_chunks.domain.video_data import VideoData


def video_producer(data: VideoData):
    element_id = '49b76588-c2ba-4166-95f9-5a59cb47a195'
    producer = KafkaProducer(bootstrap_servers=get_data()['kafka']['producer']['bootstrap-servers'],
                             key_serializer=str.encode,
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                             acks=get_data()['kafka']['producer']['acks'],
                             compression_type=get_data()['kafka']['producer']['compression-type']
                             # linger_ms=1000,
                             # batch_size=10485760
                             )
    data_as_dictionary = dataclasses.asdict(data)
    data_as_json = json.dumps(data_as_dictionary)
    json_as_bytes = data_as_json.encode('utf-8')
    print(f'sending message: {data.chunk_index}, timestamp{datetime.fromtimestamp(time.time(), tz=None)}')
    producer.send(topic=get_data()['kafka']['topics']['processed'], key=element_id, value=data_as_dictionary)


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
