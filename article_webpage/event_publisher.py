import socket
from kafka import KafkaProducer
from kafka.errors import KafkaError

import json


def publish_event(event):
    event_message = json.dumps(event)

    producer = KafkaProducer(bootstrap_servers="redpanda.blog.noether:19092")
    hostname = str.encode(socket.gethostname())

    producer.send("events", key=hostname, value=str.encode(event_message))

    producer.flush()
