import dataclasses
import json

from kafka import KafkaProducer

from configuration.configuration import get_data
from src.reader.video_data import VideoData


class VideoProducer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=get_data()['kafka']['producer']['bootstrap-servers'],
                                      # key_serializer=str.encode('utf-8'),
                                      value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                                      acks=get_data()['kafka']['producer']['acks'],
                                      compression_type=get_data()['kafka']['producer']['compression-type']
                                      )

    def produce(self, data: VideoData):
        data_as_dictionary = dataclasses.asdict(data)
        data_as_json = json.dumps(data_as_dictionary)
        json_as_bytes = data_as_json.encode('utf-8')
        self.producer.send(topic=get_data()['kafka']['topic'], value=data_as_dictionary)

