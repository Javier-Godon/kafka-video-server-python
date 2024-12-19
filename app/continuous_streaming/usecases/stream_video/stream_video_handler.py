import sys
import time

import cv2
from kafka import KafkaProducer

from app.configuration.configuration import get_data


def stream_video_producer_from_camera():
    producer = KafkaProducer(bootstrap_servers=get_data()['kafka']['producer']['bootstrap-servers'],
                             key_serializer=str.encode,
                             acks=get_data()['kafka']['producer']['acks'],
                             compression_type=get_data()['kafka']['producer']['compression-type']
                             )
    camera = cv2.VideoCapture(0)
    try:
        while True:
            success, frame = camera.read()

            ret, buffer = cv2.imencode('.jpg', frame)
            producer.send(get_data()['kafka']['topics']['streaming'], buffer.tobytes())

            # Choppier stream, reduced load on processor
            time.sleep(0.2)

    except:
        print("\nExiting.")
        sys.exit(1)

    camera.release()


stream_video_producer_from_camera()
