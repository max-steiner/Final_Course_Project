import pika


class DbRabbitConsumer:

    def __init__(self, queue_name, callback):
        self.queue_name = queue_name
        self.callback = callback
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def consume(self):
        self.channel.basic_consume( queue=self.queue_name,
                                    on_message_callback=self.callback,
                                    auto_ack=True)
        self.channel.start_consuming()