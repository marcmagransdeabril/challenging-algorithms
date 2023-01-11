import unittest
import math
import hashlib

class Bloom:
    def __init__(self,k,n):
        self.k = k
        self.hash_domain_in_bytes = math.ceil(math.log2(n)/8)   
        self.hashes_per_sha256 = 256//self.hash_domain_in_bytes
        self.n = 1 << (self.hash_domain_in_bytes*8)
        self.buffer = bytearray(self.n)

    def __indexes(self,x):
        indexes = []
        
        m = hashlib.sha256()
        d = bytearray()
        m.update(x.encode())
        for i in range(self.k // self.hashes_per_sha256 + 1):            
            m.update(str(i).encode()) # nounce to obtain the next set of hashes
            d += m.digest()
            
        for i in range(self.k):
            start = i*self.hash_domain_in_bytes
            indexes.append(int.from_bytes(d[start:start+self.hash_domain_in_bytes],"little"))
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
    def test_myers(self):
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
