Rabbitmq
========

RabbitMQ is open source message broker software (sometimes called message-oriented middleware) that implements the Advanced Message Queuing Protocol (AMQP). The RabbitMQ server is written in the Erlang programming language and is built on the Open Telecom Platform framework for clustering and failover.

Rabbitmq supports clustering and high availability features.

## Clustering.

By default all data needed by rabbitmq is replicated across the whole cluster. Messaging queues, on the other side,  are only located on the broker where they were allocated the first time. 

Rabbitmq does not perform well on WAN out of the box. There are two solutions available and delivered as plugins that can be applied to sync rabbitmq clusters and share messages on multiple DC. These are Shovel and Federation plugins.

Whereas federation aims to provide opinionated distribution of exchanges and queues, the shovel simply consumes messages from a queue on one broker, and forwards them to an exchange on another.

### Managing multiple cluster as one on different DC

#### Federation

This plugging allows us to make exchanges and queues federated. A federated exchange or queue can receive messages from one or more upstream that can be a remote exchange or queue on another broker.

**Features:**

- Loose cupling: It allows to transmit messages between clusters or brokers.
- Allows different users and virtual hosts on each cluster or brokers.
- It allows different versions of rabbitmq and erlang on each of the cluster or brokers.
- WAN Friendly: Tolerates intermittent connectivity.

##### Installation:

to enable plugin run on each broker:

```
  rabbitmq-plugins enable rabbitmq_federation
```

When using the management plugin, you will also want to enable rabbitmq_federation_management:

```
  rabbitmq-plugins enable rabbitmq_federation_management
```

Its important to mention that when using federation on a cluster all nodes must have federation enable.

##### Configuration:

There are three possible inputs of configurations:

- Upstreams: each of this defines how to connect to another broker.
- Upstream sets: group of upstreams that are use for federation.
- Policies: Are a set of exchanges and/or queues that apply to an upstream or an upstream set.

**Defining upstreams on Rabbitmq brokers:**

This can be achive via command line ctl:

```
  rabbitmqctl set_parameter federation-upstream my-upstream \
  '{"uri":"amqp://server-name","expires":3600000}'
```

or via the webUI:

```
  Navigate to Admin > Federation Upstreams > Add a new upstream. Enter "my-upstream" next to Name, "amqp://server-name" next to URI, and 36000000 next to Expires. Click Add upstream.
```

**Defining policies:**

Policies can be target on an upstream or an upstrem set. In practice upstream sets can be set to ‘all’ this way it applies federation on all upstreams.

This can also be achieved via the command line ctl:

```
  rabbitmqctl set_policy --apply-to exchanges federate-me "^amq\." \
  '{"federation-upstream-set":"all"}'
```

or via the webUI:

```
  Navigate to Admin > Policies > Add / update a policy. Enter "federate-me" next to "Name", "^amq\." next to   "Pattern", choose "Exchanges" from the "Apply to" drop down list and enter "federation-upstream-set" = "all" in the   first line next to "Policy". Click "Add" policy.
```

#### How does it work:

Clusters can be linked together with federation just as single brokers can. To summarise how clustering and federation interact:

You can define policies and parameters on any node in the downstream cluster; once defined on one node they will apply on all nodes.
Exchange federation links will start on any node in the downstream cluster. They will fail over to other nodes if the node they are running on crashes or stops.
Queue federation links will start on the same node as the downstream queue. If the downstream queue is mirrored, they will start on the same node as the master, and will be recreated on the same node as the new master if the node the existing master is running on crashes or stops.
To connect to an upstream cluster, you can specify multiple URIs in a single upstream. The federation link process will choose one of these URIs at random each time it attempts to connect.

## Numbers of nodes and roles on a Minimal cluster.

There are  2 roles that a rabbitmq broker can take which are RAM and RAM-DISK. As you can imagine RAM nodes only keep their state in memory. This does not includes queues which are always persist on disk. What a RAM broker will improve in performance is directly related with resources management (add/remove queues, exchanges and hosts). As states are replicated across all nodes in the cluster is recommended to have at least 2 disk node.

As the documentation points out [1] it is not recommended to have only one disk node. If this disk node dies the state of the cluster will be lost forever. This is why to scale up with the demand of our apps the initial clusters should include at least 3 nodes(RAM,DISK,DISK) on each DC.

Resources:

- [1] - http://www.rabbitmq.com/clustering.html
- http://www.rabbitmq.com/federation.html
- http://www.rabbitmq.com/ha.html
- http://www.rabbitmq.com/shovel.html
- https://www.rabbitmq.com/clustering.html




