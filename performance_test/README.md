RabbitMQ performance tests
==========================


## time_federation_delay test

### Requirement:
  2 clusters or brokers federated with each other.

### Running 2 rabbitmq clusters on Docker:

```
  $ cd cluster_1 && fig up 
  # this will be listening on amqp://DOCKER_SERVER_IP:5672
  $ cd cluster_2 && fig up
  # this will be listening on amqp://DOCKER_SERVER_IP:5673
```

### Usage:

```
  ./time_federation_delay.py amqp://cluster_1_ip:<PORT> amqp://cluster_2_ip:<PORT>
```

or with more specific params:

```
  ./time_federation_delay.py scheme://username:password@host:port/virtual_host?key=value&key=value scheme://username:password@host:port/virtual_host?key=value&key=value
```

### Tests steps:                                                                                                     

1. Read queue A from cluster 1 on one thread.                                                                       2. Read queue B from cluster 2 on another thread.            
3. Creates and writes current timestamp on queue A on cluster 1 on another thread.                                   4. Creates and writes current timestamp on queue B on cluster 1 on another thread.

### Output:

Whenever it reads a message it will print out the delay between the write and the read.                                                          



