class Node:
    """docstring for Nodo."""

    def __init__(self, exp=None, val=None, op=None):
        self.children = []
        self.name = 'no_name'
        self.exp = exp
        self.op = op
        self.val = val
        self.nodekind = None
        self.statement = None
        self.exp = None
        self.sibling = None
        self.type = None
        self.size = None
        self.index = None

    def __repr__(self):
        return self.name if self.name else 'Null'
