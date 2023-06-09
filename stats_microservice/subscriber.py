import pika
import json
import os
import time
from repository import dynamo


class Subscriber:
    def __init__(self, configs):
        self.config = configs

    def callback(self, ch, method, properties, body):
        print('Received message from core app')
        page = json.loads(body)
        if len(page) == 3 and page["status"] == "Deleted":
            dynamo.delete_page(user_id=page["user_id"], page_id=page["page_id"])
            print(f'Deleted page {page["page_id"]}')
        elif len(page) == 4:
            dynamo.update_page_tweets(page=page)
            print(f'Updated tweets data of page {page["page_id"]}')
        else:
            response = dynamo.get_page(user_id=page["user_id"], page_id=page["page_id"])
            if response is None:
                dynamo.add_page(page=page)
                print(f'Added page {page["page_id"]}')
            else:
                dynamo.update_page_full(page=page)
                print(f'Updated page {page["page_id"]}')

    def setup_connection(self):
        param = pika.ConnectionParameters(
            host=self.config['host'],
            port=self.config['port'],
            virtual_host="/",
            credentials=pika.PlainCredentials(
                self.config["user"],
                self.config["password"]
            ),
        )
        connection = pika.BlockingConnection(param)
        channel = connection.channel()
        channel.exchange_declare(
            exchange=self.config['exchange'],
            exchange_type=self.config['type'],
        )

        channel.queue_declare(
            queue=self.config["queue"]
        )

        # Binds the queue to the specified exchange
        channel.queue_bind(
            queue=self.config["queue"],
            exchange=self.config["exchange"],
            routing_key=self.config["routing_key"]
        )
        channel.basic_consume(
            queue=self.config["queue"],
            on_message_callback=self.callback,
            auto_ack=True
        )
        print("Waiting for data for " + self.config["queue"] + ". To exit press CTRL+C")

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()


configs = {
    "user": os.getenv('RABBITMQ_USER'),
    "password": os.getenv('RABBITMQ_PASSWORD'),
    "host": os.getenv('RABBITMQ_HOST'),
    "port": os.getenv('RABBITMQ_PORT'),
    "exchange": os.getenv('EXCHANGE_NAME'),
    "type": os.getenv('EXCHANGE_TYPE'),
    "queue": os.getenv('QUEUE_NAME'),
    "routing_key": os.getenv("ROUTING_KEY"),
}

subscriber = Subscriber(configs)

time.sleep(15)
subscriber.setup_connection()
