from main import Environment, EntryPoint, Const
from base_nodes import And_, Or_, Not_, Xor_
inp = """
def n and
def e or
def inp1 const 1
def inp2 const 1
def inp3 const 0
bind n e a
"""

env = Environment()

COMMANDS = {
    'def': env.add,
    'bind': env.bind,
}

BASE_WORDS = {
    'and': And_,
    'or': Or_,
    'not': Not_,
    'xor': Xor_,
}

DEFINITIONS = {
    'const': Const,
}

lines = inp.strip().split('\n')
words = [i.split(" ") for i in lines]
for cmd in words:
    command = cmd[:]
    for i in range(len(command)):
        if command[i] in BASE_WORDS:
            command[i] = BASE_WORDS[command[i]]()
        elif command[i] in COMMANDS:
            command[i] = COMMANDS[command[i]]
        elif command[i] in DEFINITIONS:
            value = command[i+1]
            del command[i+1]
            command[i] = DEFINITIONS[command[i]](value)
    command[0](*command[1:])
print(env._obj_heap)
print(env['n'].connections)
print(env.execute())