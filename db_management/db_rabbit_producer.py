import pika


class DbRabbitProducer:

    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def publish(self, data):
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=data)