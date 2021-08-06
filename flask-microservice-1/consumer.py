import pika, json
from main import Product, db

def main():
    parmas = pika.URLParameters('amqps://xxofsfib:V9U-0eQEjT_OBC1mOLLcJktCY6iSao90@jaguar.rmq.cloudamqp.com/xxofsfib')
    connection = pika.BlockingConnection(parmas)
    channel = connection.channel()

    channel.queue_declare(queue='main')

    def callback(ch, method, properties, body):
        print("Received in main")
        data = json.loads(body)
        print(data)

        if properties.content_type == 'product_created':
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print('Product created')

        elif properties.content_type == 'product_updated':
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print('Product Updated')
        
        elif properties.content_type == 'product_deleted':
            product = Product.query.get(data)
            db.session.delete(product)
            db.session.commit()
            print('Product Deleted')

    channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    channel.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')