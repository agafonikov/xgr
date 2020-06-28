from abc import ABC, abstractproperty, abstractmethod
from generic import Node


class BoolNodes(Node, ABC):
    def __init__(self, default_output=None):
        super().__init__()
        self.default_value = default_output
        self._current_value = default_output

    def get_value(self):
        if self.default_value is not None:
            return self.default_value
        elif not self.is_ready():
            raise ValueError("Input values are not set")
        else:
            self._current_value = self._func(**self._input_values)
            return int(self._current_value)

    def inform(self):
        for wire in self.connections:
            input_name = self.connections[wire]
            wire.inputs[input_name] = self._current_value

    @abstractproperty
    def _func(self):
        raise NotImplementedError

    @abstractmethod
    def is_ready(self):
        raise NotImplementedError

    @property
    def inputs(self):
        return self._input_values

    @inputs.getter
    def inputs_get(self):
        return self._input_values

    @inputs.setter
    def inputs_set(self, x):
        self._input_values.update(x)


class And_(BoolNodes):
    _func = lambda self, a, b: a & b

    def __init__(self, default_output=None):
        super().__init__(default_output)

    def is_ready(self):
        if  self._input_values.get('a') is not None\
        and self._input_values.get('b') is not None:
            return True
        else:
            return False

class Or_(BoolNodes):
    _func = lambda self, a, b: a | b

    def __init__(self, default_output=None):
        super().__init__(default_output)

    def is_ready(self):
        if  self._input_values.get('a') is not None\
        and self._input_values.get('b') is not None:
            return True
        else:
            return False

class Xor_(BoolNodes):
    _func = lambda self, a, b: a ^ b

    def __init__(self, default_output=None):
        super().__init__(default_output)

    def is_ready(self):
        if  self._input_values.get('a') is not None\
        and self._input_values.get('b') is not None:
            return True
        else:
            return False

class Not_(BoolNodes):
    _func = lambda self, a: not a

    def __init__(self, default_output=None):
        super().__init__(default_output)


    def is_ready(self):
        if  self._input_values.get('a') is not None:
            return True
        else:
            return False
