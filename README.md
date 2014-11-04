Rabbitmq
========

**Rabbitmq on Multiple DC via WAN.**

Rabbitmq supports clustering and high availability features.

## Clustering.

By default all data needed by rabbitmq is replicated across the whole cluster expect for messaging queues which are located on the nodes where each Chanel  are allocated the first time. 

Rabbitmq does not work well on WAN. There 2 solutions available and delivered as plugins that can be applied to sync rabbitmq clusters and share messages on multiple DC. This are Shovel and Federation plugins.


### Federation

This plugging allows us to make exchanges and queues federated. A federated exchange or queue can receive messages from one or more upstream that can be a remote exchange or queue on another broker.

** Features: **
- Loose cupling: It allows to transmit messages between clusters or brokers.
- Allows different users and virtual hosts on each cluster or brokers.
- It allows different versions of rabbitmq and erlang on each of the cluster or brokers it communicates.
- WAN Friendly: Tolerates intermittent connectivity.

#### Installation:

to enable plugin run on each broker:

```
  rabbitmq-plugins enable rabbitmq_federation
```

When using the management plugin, you will also want to enable rabbitmq_federation_management:

```
  rabbitmq-plugins enable rabbitmq_federation_management
```

Its important to mention that when using federation on a cluster all nodes must have federation enable.

#### Configuring Federation:

There are 3 possible inputs of configurations:

- Upstreams: each of this defines how to connect to another broker.
- Upstream sets: group of upstreams that are use for federation.
- Policies: Are a set of exchanges and/or queues that apply to an upstream or an upstream set.

* Defining upstreams on Rabbitmq brokers: *

This can be achive via command line ctl:

```
  rabbitmqctl set_parameter federation-upstream my-upstream \
  '{"uri":"amqp://server-name","expires":3600000}'
```

or via the webUI:

  Navigate to Admin > Federation Upstreams > Add a new upstream. Enter "my-upstream" next to Name, "amqp://server-name" next to URI, and 36000000 next to Expiry. Click Add upstream.

After this we should apply a policy on this upstream. In practice upstream sets can be set to ‘all’ this way it applies federation on all upstreams.

This can also be achieved via the command line ctl:

```
  rabbitmqctl set_policy --apply-to exchanges federate-me "^amq\." \
  '{"federation-upstream-set":"all"}'
```

or via the webUI:

  Navigate to Admin > Policies > Add / update a policy. Enter "federate-me" next to "Name", "^amq\." next to "Pattern", choose "Exchanges" from the "Apply to" drop down list and enter "federation-upstream-set" = "all" in the first line next to "Policy". Click "Add" policy.


#### Federating clusters

Clusters can be linked together with federation just as single brokers can. To summarise how clustering and federation interact:

You can define policies and parameters on any node in the downstream cluster; once defined on one node they will apply on all nodes.
Exchange federation links will start on any node in the downstream cluster. They will fail over to other nodes if the node they are running on crashes or stops.
Queue federation links will start on the same node as the downstream queue. If the downstream queue is mirrored, they will start on the same node as the master, and will be recreated on the same node as the new master if the node the existing master is running on crashes or stops.
To connect to an upstream cluster, you can specify multiple URIs in a single upstream. The federation link process will choose one of these URIs at random each time it attempts to connect.
——————————————————————————————


There are  2 roles that a rabbitmq broker can take which are RAM and RAM-DISK. As you can imagine RAM nodes only keep their state in memory. This does not includes queues which are always persist on disk. What a RAM broker will improve in performance is directly related with resources management (add/remove queues, exchanges and hosts). As states are replicated across all nodes in the cluster is recommended to have at least 2 disk node.

## Initial deploment proposal for STAGING Bluebox.

As the documentation points out [] it is not recommended to have only one disk node. If this disk node dies the state of the cluster will be lost forever. This is why to scale up with the demand of our apps the initial clusters, on east and west, should include at least 3 nodes(RAM,DISK,DISK).

The minimal recommended cluster includes 3 nodes, 2 of which are DISK-RAM and one RAM only brokers.

——————————————————————————————


http://www.rabbitmq.com/federation.html
http://www.rabbitmq.com/ha.html
http://www.rabbitmq.com/shovel.html
https://www.rabbitmq.com/clustering.html




