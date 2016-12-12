import unittest
from threading import RLock
class priority_queue:
    def __init__(self):
        self.heap_list = [0]
        self.size = 0
        self.rlock = RLock()

    def insert(self, item):
        self.rlock.acquire()
        self.heap_list.append(item)
        self.size += 1
        self.__perc_up(self.size)
        self.rlock.release()

    def __perc_up(self, index):
        while index//2 > 0:
            if self.heap_list[index] < self.heap_list[index//2]:
                self.heap_list[index // 2], self.heap_list[index] = self.heap_list[index], self.heap_list[index // 2]
            index = index//2

    def get_min(self):
        if self.size > 0:
            return self.heap_list[1]

    def del_min(self):
        self.rlock.acquire()
        if self.size > 0:
            ret_val = self.heap_list[1]
            self.heap_list[1] = self.heap_list[self.size]
            self.size -= 1
            self.heap_list.pop()
            self.__perc_down(1)
            return ret_val
        self.rlock.release()

    def __perc_down(self, index):
        def get_min_child(index):
            if index * 2 + 1 > self.size:
                return index * 2
            else:
                if self.heap_list[index * 2] < self.heap_list[index * 2 + 1]:
                    return index * 2
                else:
                    return index * 2 + 1

        while index*2 <= self.size:
            min_child = get_min_child(index)
            if self.heap_list[index] > self.heap_list[min_child]:
                self.heap_list[index], self.heap_list[min_child] = self.heap_list[min_child], self.heap_list[index]
            index = min_child

    def delete(self, item):
        self.heap_list.remove(item)
        self.size -= 1
        i = self.size//2
        while i >0:
            self.__perc_down(i)
            i-=1





    def __len__(self):
        return self.size

    def __contains__(self, item):
        return item in self.heap_list



    def __iter__(self):  #TODO returns 0 element too
        return iter(self.heap_list)

class test(unittest.TestCase):
    def test_pq(self):
        pq = priority_queue()
        pq.insert(4)
        pq.insert(5)
        pq.insert(3)
        self.assertEqual(pq.del_min(), 3)

