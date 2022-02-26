import numpy as np

class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, state_dict):
        in_open = False
        for i in range(len(self.queue)):
            if (self.queue[i]['state'] == state_dict['state']).all():
                if self.queue[i]['g'] > state_dict['g']:
                    self.queue[i] = state_dict
            in_open = True
            break

        if not in_open:
            self.queue.append(state_dict)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)
    def requeue(self, from_closed):
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):

        minf = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[minf]['f']:
                minf = i
        state = self.queue[minf]
        del self.queue[minf]
        return state

    # 0: doesn't contain, 1: contains but larger g(), 2: contains and smaller g()
    def __contains__(self, state_dict):
        for e in self.queue:
            if (e['state'] == state_dict['state']).all():
                if e['g'] > state_dict['g']:
                    return 2
                return 1

        return 0