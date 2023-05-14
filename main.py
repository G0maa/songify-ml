#!/usr/bin/env python
import pika
import sys
import os
import json
from snippet import *
# More or less src: https://www.rabbitmq.com/tutorials/tutorial-six-python.html


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    result = channel.queue_declare(queue='rpc-queue', durable=True)
    queue_name = result.method.queue

    def callback(ch, method, properties, body):
        print("properties: ", properties)
        parsed_body = json.loads(body)
        print(" [x] Received | JSONified Body %r" % parsed_body)

        print(" [x] Received | History %r" % parsed_body['history'])
        history_ids_list = switch_to_zero_based_ids(parsed_body['history'])
        print(" [x] Received | History (zero-based) %r" % history_ids_list)
        ids_list = get_recommendation_ids_list(history_ids_list)

        response_body = get_tracks_details(ids_list)

        # to-do somehow paginate the response_body
        print("Recmmended Tracks: (only first five)", response_body[:5])
        stringified_body = json.dumps(response_body)

        channel.basic_publish(exchange='', routing_key=properties.reply_to, properties=pika.BasicProperties(
            correlation_id=properties.correlation_id), body=stringified_body)
        print(" [x] Sending | JSONified Response %r" % response_body)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def switch_to_zero_based_ids(recommend_id_list):
    ids = []
    for id in recommend_id_list:
        ids.append(id - 1)

    return ids


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
