import sys


sys.path.append('../src')

from simulator import *

def main():

    for s in strategy_map:
        strategy = strategy_map[s]
        print(f'Strategy {strategy.name}:')
        print()
        sim = Simulator(4, strategy)
        sim.add_to_group([0, 2, 3], '/test')

        # This would normally be built by a distance vector router
        sim.set_routes(0, {2:{1:2,2:1,3:2},3:{1:2,2:2,3:1}})
        sim.set_routes(1, {0:{0:1,2:2,3:2},2:{0:2,2:1,3:2},3:{0:2,2:2,3:1}})
        sim.set_routes(2, {0:{0:1,1:2,3:2},3:{0:2,1:2,3:1}})
        sim.set_routes(3, {0:{0:1,1:2,2:2},2:{0:2,1:2,2:1}})

        

        starting_interests = [([0], '/test')]

        produced, dropped, kept, sent = sim.run(starting_interests)

        print()
        print("SUMMARY")
        for i in range(4):
            print(f'Node {i} produced {produced[i]}, dropped {dropped[i]}, kept {kept[i]}, sent {sent[i]}')
        
        print()
        print(f'Total produced: {sum(produced)}, total dropped: {sum(dropped)}, total kept: {sum(kept)}, total sent: {sum(sent)}')

        print()
        print()

    

    print("Simulation complete!")

if __name__ == '__main__':
    main()