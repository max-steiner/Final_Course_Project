import json
from db_management.db_data_object import DbDataObject
from db_management.db_rabbit_consumer import DbRabbitConsumer


def callback(ch, method, properties, body):
    data = json.loads(body)
    db_data = DbDataObject( airlines=int(data['airlines']),
                            customers=int(data['customers']),
                            flights_per_company=int(data['flights_per_company']),
                            tickets_per_customer=int(data['tickets_per_customer']))
    print(data)
    db_data.generate()


def main():
    rabbit = DbRabbitConsumer(queue_name='DataToGenerate', callback=callback)
    rabbit.consume()


if __name__ == '__main__':
    main()
