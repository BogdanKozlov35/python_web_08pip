import pika

from faker import Faker

from models.models import Contact


fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='messager', exchange_type='direct', durable=True)

channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange='messager', queue='email_queue')


def send_message(num_contacts):

    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        contact = Contact(full_name=full_name, email=email)
        contact.save()

        message_body = str(contact.id)
        channel.basic_publish(exchange='messager', routing_key='email_queue',
                              body=message_body, properties=pika.BasicProperties(delivery_mode=2))
        print(f"Sent contact {contact.id} to RabbitMQ")

    connection.close()


if __name__ == '__main__':

    send_message(10)