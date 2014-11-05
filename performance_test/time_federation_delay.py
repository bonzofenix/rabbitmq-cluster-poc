#!/usr/bin/env python

# Usage: 
# 	$ cluster_test cluster_1_ip<PORT> cluster_2_ip<PORT> 
#
# Requirements:
# 	Both clusters must be federated
#
# Performance tests steps:
# 	1. Read queue A from cluster 1 on one thread.
# 	2. Read queue B from cluster 2 on another thread.
# 	3. Creates and writes current timestamp on queue A on cluster 1 on another thread.
# 	3. Creates and writes current timestamp on queue B on cluster 1 on another thread.
#
# 		When message are received on any queue it calculates the diference between 
# 		current timestamp and the one of the massage and print the delay.


import pika
import thread
import sys
import time

cluster_connections = []
clusters = sys.argv

def callback(ch, method, properties, body): 
    print ch.connection.params
    print " [x] Received %s with a delay of %.3f secs \n" % ( body, (time.time() - float(body)) )

def rabbit_read(queue_name, cluster_index):
    print 'Waiting for message on queue: ' + queue_name + ' at cluster ' + str(cluster_index) + '\n'
    connection = pika.BlockingConnection(pika.URLParameters(clusters[cluster_index]))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    channel.start_consuming()

def rabbit_write(queue_name, cluster_index):
    print  'writting message on queue: ' + queue_name + ' at cluster ' + str(cluster_index) + '\n'
    connection = pika.BlockingConnection(pika.URLParameters(clusters[cluster_index]))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=( "%.6f" % time.time()))
    connection.close()
	
try: 
    thread.start_new_thread( rabbit_read, ('queue_a',1, ))
    thread.start_new_thread( rabbit_read, ('queue_b',2, ))
    thread.start_new_thread( rabbit_write, ('queue_a',1, ))
    thread.start_new_thread( rabbit_write, ('queue_b',1, ))

except:
   print "Error: unable to start thread"

while 1:
   pass

