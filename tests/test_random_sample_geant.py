import sys
from minindn_to_nodes import *
from random import randint


sys.path.append('../src')

from simulator import *
from routing import *

def main():

    for i in range(1000):
        group_size = randint(2, 43)
        group_members = []
        while group_size > 0:
            member = randint(0, 44) # Number of nodes
            if member not in group_members:
                group_members.append(member)
                group_size -= 1
        
        # Choose a random group member to produce an interest
        starting_interests = [([group_members[randint(0, len(group_members)-1)]], "/test")]

        config_file = "topo_geant.conf"
        
        nodes, routes = converge(group_members, config_file)

        #print(routes)

        for s in strategy_map:
            strategy = strategy_map[s]
            print(f'Strategy {strategy.name}:')
            print()
            sim = Simulator(len(nodes), strategy)
            sim.add_to_group(group_members, '/test')

            # This would normally be built by a distance vector router
            for r in routes:
                #print(r, routes[r])
                sim.set_routes(r, routes[r])

            produced, dropped, kept, sent = sim.run(starting_interests)

            print()
            print("SUMMARY")
            for i in range(len(nodes)):
                print(f'Node {i} produced {produced[i]}, dropped {dropped[i]}, kept {kept[i]}, sent {sent[i]}')
            
            print()
            print(f'Total produced: {sum(produced)}, total dropped: {sum(dropped)}, total kept: {sum(kept)}, total sent: {sum(sent)}')

            print()
            print()

        

        print("Simulation complete!")

if __name__ == '__main__':
    main()