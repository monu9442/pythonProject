import os

import pika
import json

from app.config.queue import QueueCredentials


def create_queue_connection(host_ip, user, password, port):
    try:
        credentials = pika.PlainCredentials(user, password)
        parameters = pika.ConnectionParameters(str(host_ip), port, '/', credentials, heartbeat=600, blocked_connection_timeout=600)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        return connection, channel
    except Exception as error:
        print("Error: Connection not established {}".format(error))


class QueueConnector:

    def __init__(self):
        self.host = QueueCredentials.host
        self.port = QueueCredentials.port
        self.user = QueueCredentials.user
        self.password = QueueCredentials.password
        self.real_time_full_indexing_queue = os.environ.get("PUSH_QUEUE")
        self.prefetch_value = int(os.environ.get("PREFETCH_VALUE"))
        self.create_connections()

    def create_connections(self):
        self.connection, self.channel = create_queue_connection(self.host, self.user, self.password, self.port)

    def close_connection(self):
        self.connection.close()

    def publish_data(self, body):
        log_data = {"push_message_body_to_altair": body}
        # mqConnection = QueueConnector()
        self.channel.basic_publish(
            exchange='',
            routing_key=self.real_time_full_indexing_queue,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))

    def get_message_for_publish(self, id, index_name, data_type, source = None):
        return {"id": id, "index": index_name, "type": data_type, "source":source}


RabbitMqConnector = QueueConnector()
