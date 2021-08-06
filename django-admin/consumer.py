import pika, sys, os, json, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microservices.settings")
django.setup()

from products.models import Product

def main():
    parmas = pika.URLParameters('amqps://xxofsfib:V9U-0eQEjT_OBC1mOLLcJktCY6iSao90@jaguar.rmq.cloudamqp.com/xxofsfib')
    connection = pika.BlockingConnection(parmas)
    channel = connection.channel()

    channel.queue_declare(queue='admin')

    def callback(ch, method, properties, body):
        print("Received in admin")
        id = json.loads(body)
        print('el id:', id)
        product = Product.objects.get(id=id)
        product.likes = product.likes + 1
        product.save()
        print("Products like increase!")

    channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    channel.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')