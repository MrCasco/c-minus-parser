class Node:
    """docstring for Nodo."""

    def __init__(self, exp=None, val=None, op=None):
        self.children = []
        self.exp = exp
        self.op = op
        self.val = val
