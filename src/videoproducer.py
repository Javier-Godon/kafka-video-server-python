import dataclasses
import json
import time
from datetime import datetime

from kafka import KafkaProducer

from configuration.configuration import get_data
from src.reader.video_data import VideoData


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
    producer.send(topic=get_data()['kafka']['topic'], key=element_id, value=data_as_dictionary)
