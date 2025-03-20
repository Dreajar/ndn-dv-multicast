# Introduction
This project attempts to find a forwarding strategy that improves upon the current forwarding strategy in ndn-dv, where a node forwards to all neighbors through which a group member can be reached.

We do this via a routing/forwarding simulator that simplifies the process of testing a strategy on many topologies. We do not simulate delay or link costs, the simulator only runs through each node sequentially and asks them to forward any interests they have, until a cycle occurs where no nodes forward any interests.
The simulator also tracks metrics for the current run for comparison purposes.

## Forwarding strategies
forwarder.py contains two routing strategies, and adding more should be as simple as creating a new routing class and adding it to the strategy_map.

## Writing Tests
There are two ways to write a test:

### Hardcoding Routing Info
An example of this is test_1.py. Use the set_routes() function from the Simulator class to directly input the routing information. This will be very inefficient for larger topologies, and was mostly used to test the automatic routing algorithm.

### Using Bellman-Ford
An example of this is test_sprint.py. The file topo.sprint.conf is one of the stock miniNDN config files. 
To create a new topology for this type of test, create a miniNDN-style config file by specifying the names of the nodes and the links between them. Using the bellman_ford() function in routing.py, the routing algorithm will automatically assign a nodeID to each node and build the topology, then perform Bellman-Ford routing to build the RIB for each node. Note that each node only cares about the routes to each group member.

Note that the simulator currently only supports one group prefix at a time, supporting multiple is a possible extension that can be made in the future.

### Setting up the rest
In test_sprint.py, we have to set group_members and config_file as parameters to the Bellman-Ford algorithm.
The other important parameter is starting_interests, which tells the simulator which nodes will produce an interest, and the prefix (not fully functional, just use '/test').

## Running a Test
To run a test, cd into the /tests folder and type:
```
python3 {test_name}.py
```

## Reading the Output
Each test will run both strategies **(send all, lowest cost)** and log the output of each run.
Anytime an interest is sent, dropped, or the simulator detects it has reached all nodes, the simulator will log it.

At the end of each run, a summary will be printed showing how many interests were produced, dropped, kept (received/not dropped), and sent by each node, and in total.
This allows for easy comparison between the two strategies.

If at the end of the run an interest has not reached all group members, the simulator will let you know.
This scenario means that the forwarding strategy was incorrect, meaning not all group members received the interest once the forwarding "cycle" has converged.