"""
Author Daniel Riegelhaupt
November 2014

A simple position object.
Needed to be able to search in trees using line and column
"""

class Position(object):
    """
    a position object with the comparison operators implemented so that we can use the position to search
    for backwards compatibility the operator [] has also been overridden
    ["line"] or ["row"] will get/set self.line and ["column"] or ["col"] will get or set self.column
    This is not needed and self.line or column can be accesed directly as well
    """
    def __init__(self, line, col):
        self.line = line
        self.column = col

    def toDictionary(self):
        return { 'line': self.line, 'column': self.column}

    def __repr__(self):
        return  "{'line': " + str(self.line)  +", 'column': " + str(self.column) +"}"

    def __str__(self):
        #return str({ 'line' : self.line , 'column' : self.column })
        return "{'line': " + str(self.line)  +", 'column': " + str(self.column) +"}"

    def __eq__(self, other):
        # ==
        return ((self.line == other.line) and (self.column == other.column))

    def __lt__(self, other):
        # <
        return ((self.line < other.line) or ((self.line == other.line) and (self.column < other.column)))

    def __le__(self, other):
        # <=
        return ((self.line < other.line) or ((self.line == other.line) and (self.column <= other.column)))

    def __ne__(self, other):
        # !=
        return ((self.line != other.line) or (self.column != other.column))

    def __gt__(self, other):
        # >
        return ((self.line > other.line) or ((self.line == other.line) and (self.column > other.column)))

    def __ge__(self, other):
        # <=
        return ((self.line > other.line) or ((self.line == other.line) and (self.column >= other.column)))

    def __getitem__(self, item):
        # varname = position['line']
        if item == 'line' or item == 'row':
            return self.line
        elif item == 'column' or item == 'col':
            return self.column
        else:
            raise AttributeError("'Position' object has no attribute '"+str(item)+"'")

    def __setitem__(self, item, value):
        # position['line'] = 5
        if item == 'line' or item == 'row':
            self.line = value
        elif item == 'column' or item == 'col':
            self.column =value
        else:
            raise AttributeError("'Position' object has no attribute '"+str(item)+"'")

    def deepcopy(self):
        return Position(self.line, self.col)