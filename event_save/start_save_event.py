from kafka import KafkaConsumer
import logging
import base64, json, time

logger = logging.getLogger("event_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("events.log")
logger.addHandler(file_handler)

def get_event_payload(event):
    b64_str = event["payload"]
    payload_json_str = base64.b64decode(b64_str).decode("utf-8")
    return json.loads(payload_json_str)


def log_event(event):
    print(event["event_id"])
    logger.info(f"Received event {event['event_id']} - {event['corelation_id']}")


consumer = KafkaConsumer(
    bootstrap_servers=["redpanda.blog.noether:19092"],
    group_id="event_logger",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    consumer_timeout_ms=1000,
)

consumer.subscribe("events")

while True:
    print("Consume messages")
    for message in consumer:
        print("consume")
        event_json_str = message.value.decode("utf-8")
        event = json.loads(event_json_str)
        log_event(event)

    time.sleep(5)
