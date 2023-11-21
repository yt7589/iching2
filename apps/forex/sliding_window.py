#

class SlidingWindow(object):
    def __init__(self, len):
        self.data = [0 for i in range(len)]
        self.cnt = 0
        self.capacity = len
    def add(self, element):
        self.data.pop(0)
        self.data.append(element)
        if self.cnt >= self.capacity:
            self.cnt = self.capacity
        else:
            self.cnt += 1
    def last(self):
        return self.data[-1]
    def previous(self):
        return self.data[-2]