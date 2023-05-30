import unittest
import math
import hashlib

class Bloom:
    def __init__(self,k,n):
        self.k = k
        self.hash_domain_in_bits = math.ceil(math.log2(n))   
        assert self.hash_domain_in_bits < 256
        self.mask = int("".join(["1"]*self.hash_domain_in_bits),2)
        self.n = 1 << self.hash_domain_in_bits
        self.buffer = bytearray(self.n)
        

    def __indexes(self,x):
        indexes = []
        
        m = hashlib.sha256()
        d = bytearray()
        m.update(x.encode())
        for i in range(self.k):
            indexes.append(int.from_bytes(m.digest(),byteorder='little',signed=False) & self.mask)         
            m.update(str(i).encode()) # nounce to obtain the next set of hashes

        return indexes

    def __contains__(self,x):
        indexes = self.__indexes(x)
        
        return all([self.buffer[i//8] & (1 << (i % 8 ) ) != 0 for i in indexes])

    def add(self,x):
        indexes = self.__indexes(x)
        for i in indexes:
            self.buffer[i//8] |= 1 << (i % 8 )

    def clear(self):
        self.buffer = bytearray(self.n)


class Testing(unittest.TestCase):
    def test_bloom(self):
        b=Bloom(3,10000)
        b.add("hello")
        self.assertTrue("hello" in b)
        self.assertFalse("world" in b)

        b.clear()
        self.assertFalse("hello" in b)

        b.add("hello")
        self.assertTrue("hello" in b)
        self.assertFalse("world" in b)
        b.add("world")
        self.assertTrue("world" in b)
