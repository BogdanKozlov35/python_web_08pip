import pika
from bson import ObjectId
from models.models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='messager', exchange_type='direct', durable=True)

channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange='messager', queue='email_queue')

channel.queue_declare(queue='email_queue', durable=True)


def send_email(ch, method, properties, body):
    body_str = body.decode('utf-8')
    contact_id = ObjectId(body_str)
    contact = Contact.objects(id=contact_id).first()

    if contact:

        print(f"Sending email to {contact.email}...")

        contact.message_sent = True
        contact.save()
        print(f"Message sent to {contact.email}. Updated status to True.")
    else:
        print(f"Contact with id {contact_id} not found in database.")

    ch.basic_ack(delivery_tag=method.delivery_tag)

# channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_queue', on_message_callback=send_email)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()