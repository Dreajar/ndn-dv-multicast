import sys


sys.path.append('../src')

from simulator import *

def main():

    for s in strategy_map:
        strategy = strategy_map[s]
        print(f'Strategy {strategy.name}:')
        print()
        sim = Simulator(12, strategy)
        sim.add_to_group([2, 6, 11], '/test')

        # This would normally be built by a distance vector router
        sim.set_routes(0, {2:{1:2}, 6:{1:4}, 11:{1:5}})
        sim.set_routes(1, {2:{2:1},6:{4:3},11:{4:4}})
        sim.set_routes(2, {6:{1:4},11:{1:5}})
        sim.set_routes(3, {2:{4:3,6:5},6:{4:3,6:1},11:{4:4,6:4}})
        sim.set_routes(4, {2:{1:2},6:{3:2,7:2},11:{3:5,7:3}})
        sim.set_routes(5, {2:{4:3},6:{4:3},11:{4:4}})
        sim.set_routes(6, {2:{3:4,7:4},11:{3:5,7:2}})
        sim.set_routes(7, {2:{4:3,6:5},6:{4:3,6:1},11:{10:2}})
        sim.set_routes(8, {2:{0:3,7:4},6:{0:5,7:2},11:{0:6,7:3}})
        sim.set_routes(9, {2:{10:5},6:{10:3},11:{10:2}})
        sim.set_routes(10, {2:{7:4},6:{7:2},11:{11:2}})
        sim.set_routes(11,{2:{10:5},6:{10:3}})

        starting_interests = [([2], '/test')]

        produced, dropped, kept, sent = sim.run(starting_interests)

        print()
        print("SUMMARY")
        for i in range(12):
            print(f'Node {i} produced {produced[i]}, dropped {dropped[i]}, kept {kept[i]}, sent {sent[i]}')
        
        print()
        print(f'Total produced: {sum(produced)}, total dropped: {sum(dropped)}, total kept: {sum(kept)}, total sent: {sum(sent)}')

        print()
        print()

    

    print("Simulation complete!")

if __name__ == '__main__':
    main()