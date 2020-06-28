from generic import Node, Const, EntryPoint
from base_nodes import And_, Not_, Or_, Xor_
from collections import OrderedDict



class Environment:
    def __init__(self):
        self._obj_heap = dict()

    def execute(self, times:int=1):
        initial_queue = {k: v for k, v in self._obj_heap.items() if v.is_ready() and not issubclass(v.__class__, EntryPoint)}
        iteration_results = []
        for _ in range(0, times):
            iteration_results.append(self._make_iteration(initial_queue))
        return iteration_results

    def _make_iteration(self, init_queue: OrderedDict) -> OrderedDict:
        queue = init_queue.copy()
        done = {k: v for k, v in self._obj_heap.items() if issubclass(v.__class__, EntryPoint)}
        result = OrderedDict()
        while len(queue) is not 0:
            new_states, new_queue = self._execute_nodes(queue, done)
            result.update(new_states)
            queue = new_queue
        return result

    def _execute_nodes(self, queue, done):
        states = OrderedDict()
        new_queue = OrderedDict()
        for name, node in queue.items():
            if name not in done:
                states.update({name: node.get_value()})
                node.inform()
                done.update({name: node})
                for k, _ in node.connections.items():
                    if k.is_ready():
                        new_queue.update({list(self._obj_heap.keys())[list(self._obj_heap.values()).index(k)]: k})
        return (states, new_queue)


    def add(self, name:str, obj:Node) -> None:
        if issubclass(obj.__class__, Node):
            self._obj_heap.update({name: obj})
        else:
            raise AttributeError("Only Node derivatives allowed in Environment")

    def __getitem__(self, key) -> Node:
        return self._obj_heap[key]

    def bind(self, from_node, to_node, input_name):
        self[from_node].bind(input_name, self[to_node])

class Block(Environment, Node):
    pass

if __name__ == "__main__":
    env = Environment()
    env.add('inp1', Const(True))
    env.add('inp2', Const(False))

    env.add('r', And_())
    env.add('s', And_())
    env.add('q', Not_())
    env.add('nq', Not_())

    env['s'].bind('a', env['q'])


    env['inp1'].bind('a', env['s'])
    env['inp2'].bind('b', env['s'])
    print(env.execute(3))

