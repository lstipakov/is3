#!/usr/bin/env python
import pika
from is_srv_f import *
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='est')

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep(10)
    send_OK('calculated')

channel.basic_consume(callback,queue='est')

channel.start_consuming()
