import pika, json

params = pika.URLParameters('amqps://xxofsfib:V9U-0eQEjT_OBC1mOLLcJktCY6iSao90@jaguar.rmq.cloudamqp.com/xxofsfib')
#params.socket_timeout = 5
connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', 
        routing_key='main', 
        body=json.dumps(body), 
        properties=properties
    )