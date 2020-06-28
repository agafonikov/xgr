from abc import ABC, abstractmethod, abstractproperty

class Node(ABC):
    def __init__(self) -> None:
        self._input_values = {}
        self.connections = {}
        self._current_value = None

    def inform(self) -> None:
        for wire in self.connections:
            input_name = self.connections[wire]
            wire.inputs[input_name] = self._current_value

    def bind(self, parameter_name, node):
        self.connections[node] = parameter_name

    @abstractmethod
    def get_value(self) -> any:
        raise NotImplementedError

    @abstractmethod
    def is_ready(self) -> bool:
        '''  '''
        raise NotImplementedError

    @abstractproperty
    def inputs(self):
        raise NotImplementedError

    @abstractproperty
    def inputs_get(self, x):
        raise NotImplementedError

    @abstractproperty
    def inputs_set(self):
        raise NotImplementedError


class EntryPoint(Node):
    '''
    Entry points are nodes that has values since the start of execution.
    Values might be changed between iterations of execution graph
    '''
    def __init__(self):
        super().__init__()

    def is_ready(self):
        '''Entry point always has a value'''
        return True

    @property
    def inputs(self):
        pass

    @inputs.getter
    def inputs_get(self):
        return None

    @inputs.setter
    def inputs_set(self, x):
        raise AttributeError("Read only property")

    def bind(self, parameter_name, node):
        '''
        Binding method for EntryPoint immediately informs child nodes about his value
        '''
        self.connections[node] = parameter_name
        self.inform()

class Const(EntryPoint):
    def __init__(self, value):
        super().__init__()
        self._current_value = value

    def get_value(self):
        return int(self._current_value)