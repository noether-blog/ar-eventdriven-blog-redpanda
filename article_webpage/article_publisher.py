from datetime import datetime
from event_publisher import publish_event
import random, string, json, base64


def publish(article):
    current_date = datetime.now()
    utc_date_str = current_date.strftime("%Y%m%d-%H%M%S")

    article_to_pusblish = {
        "title": article["title"],
        "content": article["content"],
        "author": article["author"],
        "tag": article["tags"],
        "written_date": utc_date_str,
    }

    event = build_event_for_article(article_to_pusblish)
    publish_event(event)


def build_event_for_article(article):
    return {
        "event_id": generate_event_id(),
        "event_type": "new-article",
        "payload": event_payload_from(article),
        "parent_event_id": "Initial",
        "corelation_id": generate_corelation_id()
    }


def event_payload_from(article):
    article_json_string = json.dumps(article)
    article_json_to_byte = article_json_string.encode("utf-8")
    return base64.b64encode(article_json_to_byte).decode("utf-8")

def generate_random_string(length):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))

def generate_event_id():
    current_date = datetime.now()
    utc_date_str = current_date.strftime("%Y%m%d-%H%M%S")

    event_signature = generate_random_string(15)

    return f"new-article-{utc_date_str}-{event_signature}"

def generate_corelation_id():
    return f"corel_{generate_random_string(10)}"
