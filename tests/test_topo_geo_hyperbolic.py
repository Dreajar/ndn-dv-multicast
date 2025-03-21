import sys
from minindn_to_nodes import *


sys.path.append('../src')

from simulator import *
from routing import *
from powerset import *

def main():

    # Get config file, parse and turn into routing info via Bellman-Ford
    config_file = "topo_geo_hyperbolic.conf"
    group_members_combination = powerset(5)
    for group_members in group_members_combination:
        print(group_members)
        
        
    
        nodes, routes = converge(group_members, config_file)

        print(routes)

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

            starting_interests = [([group_members[0]], '/test')]

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