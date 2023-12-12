from kafka import KafkaConsumer, KafkaProducer 
import base64, json, time, random, string, socket
from datetime import datetime


def generate_random_string(length):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))


def get_event_payload(event):
    b64_str = event["payload"]
    payload_json_str = base64.b64decode(b64_str).decode("utf-8")
    return json.loads(payload_json_str)

def compute(article):
    content = article['title']
    content += "\r"
    content += "---"
    content += "\r\r"
    content += article['content']
    content += "\r\r"
    content += "---\r"
    content += f"Written By {article['author']}\r\r"
    content += f"Tags {article['tag']}\r\r"
    content += f"On {article['written_date']}"
    return content

def save_article(article):
    
    article_content = compute(article)

    with open(f'articles/{generate_random_string(10)}.demo.md', "w") as article_file:
        article_file.write(article_content)

    article_save_result = "SUCCESS"

    details = {"id": "None", "message": "Cannot save article because of reasons"}

    if article_save_result == "SUCCESS":
        details = {
            "id": generate_random_string(10),
            "message": "Article saved successfully",
        }

    return {"status": article_save_result, "details": details}


def publish_saved_article_event(save_result, parent_event):
    event = {
        "event_id": generate_event_id(),
        "event_type": "article-saved",
        "payload": event_payload_from(save_result),
        "parent_event_id": parent_event["event_id"],
        "corelation_id": parent_event["corelation_id"]
    }

    publish_event(event)


def generate_event_id():
    def generate_random_string(length):
        letters = string.ascii_letters
        return "".join(random.choice(letters) for _ in range(length))

    current_date = datetime.now()
    utc_date_str = current_date.strftime("%Y%m%d-%H%M%S")

    event_signature = generate_random_string(15)

    return f"article-saved-{utc_date_str}-{event_signature}"


def event_payload_from(article):
    article_json_string = json.dumps(article)
    article_json_to_byte = article_json_string.encode("utf-8")
    return base64.b64encode(article_json_to_byte).decode("utf-8")


def publish_event(event):
    event_message = json.dumps(event)

    producer = KafkaProducer(bootstrap_servers="redpanda.blog.noether:19092")
    hostname = str.encode(socket.gethostname())

    producer.send("events", key=hostname, value=str.encode(event_message))
    producer.flush()

    print("Save event sent")


consumer = KafkaConsumer(
    bootstrap_servers=["redpanda.blog.noether:19092"],
    group_id="save_article",
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

        print(f"{event['event_type']}")

        if event['event_type'] != 'new-article':
            continue

        event_payload = get_event_payload(event)
        save_result = save_article(event_payload)
        publish_saved_article_event(save_result, event)

    time.sleep(5)
