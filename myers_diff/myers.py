import unittest
import heapq

def diff(a, b):
    N = len(a)
    M = len(b)

    visit = set()
    q = []

    heapq.heappush(q,(0, 0, 0, [] ))

    while q:
        d,i,j,history = heapq.heappop(q)
        if (i,j) in visit:
            continue
        
        visit.add((i,j))
        while i<N and j<M and a[i] == b[j]:
            visit.add((i,j))
            i += 1
            j += 1

        if i == N and j == M:
            return history

        if i < N and (i+1,j) not in visit:
            heapq.heappush(q,(d+1, i+1, j, history + ["- " + a[i] ] ))
        if j < M and (i,j+1) not in visit:
            heapq.heappush(q,(d+1, i, j+1, history + ["+ " + b[j] ] ))
        





class Testing(unittest.TestCase):
    def test_myers(self):
        a = ["A","B"]
        b = ["A","B","B"]

        self.assertEqual(diff(a,b), ["+ B"])

        a = ["A","B","B"]
        b = ["A","B"]

        self.assertEqual(diff(a,b), ["- B"])

        a = ["B","B"]
        b = ["A","B"]

        self.assertEqual(diff(a,b), ["- B","+ A"])

        a = ["A","B"]
        b = ["A","B"]

        self.assertEqual(diff(a,b), [])

        a = ["A","A","B","A","B"]
        b = ["A","B"]

        self.assertEqual(diff(a,b), ["- A","- A","- B"])

        a = ["A","B"]
        b = ["A","A","B","A","B"]

        self.assertEqual(diff(a,b), ["+ A","+ A","+ B"])


