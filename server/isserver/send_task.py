#!/usr/bin/env python
import pika

def send_msg(is_msg, is_queue='hello', is_host = 'localhost'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=is_host))
    channel = connection.channel()
    channel.queue_declare(queue=is_queue)
    channel.basic_publish(exchange='',
                      routing_key=is_queue,
                      body=is_msg)
    print " [x] Sent", is_msg
    connection.close()
