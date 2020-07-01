import heapq as minq


class maxq:
    """Maximum oriented heap priority queue using the builtin heapq. Supports methods heappop, heapify and heappush"""
    heappop = minq._heappop_max
    heapify = minq._heapify_max

    @staticmethod
    def heappush(heap, item):
        heap.append(item)
        minq._siftdown_max(heap, 0, len(heap)-1)


class FastMedian:
    """Object optimized for fast median retrieval. Stores comparable elements in heaps max_pq and min_pq
    where max_pq[0] <= min_pq[0]
    balance:
        len(max_pq) = len(min_pq) - 1
    """
    def __init__(self, array=None):
        self.min_pq = []
        self.max_pq = []
        if array:
            for i in array:
                self._push(i)
            self._balance()

    def elements(self):
        """Iterator over the elements"""
        return iter(self.max_pq + self.min_pq)

    def median(self):
        """Returns the current median. Not to be called on empty."""
        if len(self.min_pq) == len(self.max_pq):
            return round((self.min_pq[0] + self.max_pq[0]) / 2, ndigits=2)
        return self.min_pq[0]

    def insert_list(self, items):
        """As push and then it will balance, this will not increase the data count"""
        out = 0
        for item in items:
            self._push(item)
            out += item
        self._balance()
        return out

    def insert(self, item):
        """As push and then it will balance, this will not increase the data count"""
        self._push(item)
        self._balance()

    def _push(self, item):
        """Push the item in to the data without balancing, this increases the data count"""
        if not self.min_pq or item > self.min_pq[0]:
            minq.heappush(self.min_pq, item)
        else:
            maxq.heappush(self.max_pq, item)

    def clear(self):
        """Effectively removes two items from the data. It returns pops the median, it also removes the
        lower median while balancing."""
        self.min_pq = []
        self.max_pq = []

    def _balance(self):
        """Balance the max and min priority queue to satisfy the equation:
            0 <= len(min_pq) - len(max_pq) <= 1
        where the elements are:
            max_pq < min_pq[0] <= min_pq[1:]
        """
        min_l = len(self.min_pq)
        max_l = len(self.max_pq)
        while min_l - max_l not in [0, 1] and self.min_pq:
            if max_l > min_l:
                minq.heappush(self.min_pq, maxq.heappop(self.max_pq))
                max_l -= 1
                min_l += 1
            else:
                maxq.heappush(self.max_pq, minq.heappop(self.min_pq))
                max_l += 1
                min_l -= 1
