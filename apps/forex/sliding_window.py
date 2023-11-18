#

class SlidingWindow(object):
    def __init__(self, len):
        self.data = [0 for i in range(len)]
    def add(self, element):
        self.data.pop(0)
        self.data.append(element)
    def last(self):
        return self.data[-1]
    def previous(self):
        return self.data[-2]