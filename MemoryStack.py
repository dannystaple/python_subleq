"""A memory mapped stack implementation"""
__author__ = 'stapled'

class MemoryStack(object):
    def __init__(self):
        self.stack = []

    def __setitem__(self, key, value):
        if key == 0:
            self.stack.append(value)
        else:
            raise IndexError()

    def __getitem__(self, key):
        if key == 0:
            return self.stack.pop()
        else:
            raise IndexError()


