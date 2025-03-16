import sys


sys.path.append('../src')

from simulator import *

def main():

    for s in strategy_map:
        strategy = strategy_map[s]
        print(f'Strategy {strategy.name}:')
        print()
        sim = Simulator(7, strategy)
        sim.add_to_group([0, 5, 6], '/test')

        # This would normally be built by a distance vector router
        sim.set_routes(0, {5: {1: 2, 2: 5}, 6: {1: 3, 2: 4}})
        sim.set_routes(1, {0: {0: 1, 4: 4, 5: 6}, 5: {0: 6, 4: 3, 5: 1}, 6: {0: 3, 4: 2, 5: 2}})
        sim.set_routes(2, {0: {0: 1, 3: 4}, 5: {0: 3, 3: 4}, 6: {0: 4, 3: 3}})
        sim.set_routes(3, {0: {2: 2, 4: 3}, 5: {2: 4, 4: 3}, 6: {2: 4, 4: 3}})
        sim.set_routes(4, {0: {1: 2, 3: 3, 6: 4}, 5: {1: 2, 3: 5, 6: 2}, 6: {1: 3, 3: 6, 6: 1}})
        sim.set_routes(5, {0: {1: 2, 6: 5}, 6: {1: 3, 6: 1}})
        sim.set_routes(6, {0: {4: 3, 5: 3}, 5: {4: 3, 5: 1}})

        starting_interests = [([0], '/test')]

        produced, dropped, kept, sent = sim.run(starting_interests)

        print()
        print("SUMMARY")
        for i in range(7):
            print(f'Node {i} produced {produced[i]}, dropped {dropped[i]}, kept {kept[i]}, sent {sent[i]}')
        
        print()
        print(f'Total produced: {sum(produced)}, total dropped: {sum(dropped)}, total kept: {sum(kept)}, total sent: {sum(sent)}')

        print()
        print()

    

    print("Simulation complete!")

if __name__ == '__main__':
    main()