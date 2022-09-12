import pika
from django.conf import settings


class Publisher:
    def __init__(self, configs):
        self.config = configs

    def publish(self, message):
        connection = self.create_connection()

        # Create a new channel with the next available channel number or pass in a channel number to use
        channel = connection.channel()

        # Creates an exchange if it does not already exist, and if the exchange exists,
        # verifies that it is of the correct and expected class.

        channel.exchange_declare(
            exchange=self.config["exchange"],
            exchange_type=self.config["type"],
        )

        channel.queue_declare(
            queue=self.config["queue"]
        )

        # Publishes message to the exchange with the given routing key
        channel.basic_publish(
            exchange=self.config["exchange"],
            routing_key=self.config["routing_key"],
            body=message
        )

        print(f"Sent {message}")

    # Create new connection
    def create_connection(self):
        param = pika.ConnectionParameters(
            host=self.config['host'],
            port=self.config['port'],
            virtual_host="/",
            credentials=pika.PlainCredentials(
                self.config["user"],
                self.config["password"]
            ),
        )
        return pika.BlockingConnection(param)


configs = {
    "user": settings.RABBITMQ_USER,
    "password": settings.RABBITMQ_PASSWORD,
    "host": settings.RABBITMQ_HOST,
    "port": settings.RABBITMQ_PORT,
    "exchange": settings.EXCHANGE_NAME,
    "type": settings.EXCHANGE_TYPE,
    "queue": settings.QUEUE_NAME,
    "routing_key": settings.ROUTING_KEY,
}

# create publisher instance
publisher = Publisher(configs)
# usage example: publisher.publish(‘New Data’)


