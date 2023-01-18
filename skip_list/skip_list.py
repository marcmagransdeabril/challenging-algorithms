from collections import namedtuple
import unittest
import random

MAXLEVEL = 16
P = 1/2

class Node:
    def __init__(self,key,value,forward):
        self.key=key
        self.value=value
        self.forward=forward

    def __str__(self):
        return "({},{},[{}])".format(self.key,self.value,",".join([ str(s) for s in self.forward]))


class SkipList:
    

    def __init__(self):
        self.header = Node(None,None,[None]*MAXLEVEL)
        self.level = 0
        self.len=0

    def __randomLevel(self):
        lvl = 1
        while random.random() < P and lvl < MAXLEVEL:
            lvl = lvl + 1 
        return lvl

    def __setitem__(self, searchKey, value):
        update = [None]*MAXLEVEL
        x = self.header

        for i in range(self.level-1,-1,-1):
            while x.forward[i] and x.forward[i].key < searchKey:
                x = x.forward[i]
            update[i] = x
        x = x.forward[0]

        if x and x.key == searchKey:
            x.value = value
        else:
            lvl = self.__randomLevel()
            #print(lvl)

            if lvl > self.level:
                for i in range(self.level,lvl):
                    update[i] = self.header

                self.level = lvl

            x = Node(searchKey,value,[None]*lvl)

            for i in range(lvl):
                x.forward[i] = update[i].forward[i]
                update[i].forward[i] = x
            
            self.len += 1
            #print(self.header)

    def __contains__(self,key):
        return self.__getitem(key) is not None

    def __iter__(self):
        self.iter = self.header.forward[0]
        return self

    def __next__(self):
        if self.iter is None:
            raise StopIteration()

        x = self.iter
        self.iter = x.forward[0]
        return x.key

        

    def __len__(self):
        return self.len


    def __getitem(self, searchKey):
        x = self.header
        for i in range(self.level-1,-1,-1):
            while x.forward[i] and x.forward[i].key < searchKey:
                x = x.forward[i]

        x = x.forward[0]

        if x and x.key == searchKey:
            return x.value
        else:
            return None

    def __getitem__(self, key):
        x = self.__getitem(key)
        if x is None:
            raise KeyError("key '{}' not found".format(key))

        return x
    
    def clear(self):
        self.__init__()

    def pop(self, searchKey):
        update = [None]*MAXLEVEL
        x = self.header

        for i in range(self.level-1,-1,-1):
            while x.forward[i] and x.forward[i].key < searchKey:
                x = x.forward[i]
            update[i] = x
        x = x.forward[0]

        if x and x.key == searchKey:
            for i in range(self.level):
                if update[i].forward[i] != x:
                    break
                update[i].forward[i] = x.forward[i]
            
            while self.level >= 1 and self.header.forward[self.level-1] is None:
                self.level -= 1

            self.len -= 1
        else:
            raise KeyError("key '{}' not found".format(searchKey))





class Testing(unittest.TestCase):
    def test_skiplist(self):
        s = SkipList()
        self.assertFalse("a" in s)
        s["a"] = 1
        self.assertEqual(len(s),1)
        self.assertTrue("a" in s)
        self.assertEqual(s["a"],1)
        self.assertFalse("b" in s)
        with self.assertRaises(KeyError):
            s["b"]

        s["b"] = 2
        self.assertEqual(len(s),2)
        self.assertTrue("a" in s)
        self.assertTrue("b" in s)
        self.assertEqual(s["a"],1)
        self.assertEqual(s["b"],2)
        self.assertFalse("c" in s)
        with self.assertRaises(KeyError):
            s["c"]  
        
        s["c"] = 3
        self.assertEqual(len(s),3)
        self.assertTrue("a" in s)
        self.assertTrue("b" in s)
        self.assertTrue("c" in s)
        self.assertEqual(s["a"],1)
        self.assertEqual(s["b"],2)
        self.assertEqual(s["c"],3)
        self.assertFalse("d" in s)
        with self.assertRaises(KeyError):
            s["d"]  

        s["aa"] = 4
        self.assertEqual(len(s),4)
        self.assertTrue("a" in s)
        self.assertTrue("b" in s)
        self.assertTrue("c" in s)
        self.assertTrue("aa" in s)
        self.assertEqual(s["a"],1)
        self.assertEqual(s["b"],2)
        self.assertEqual(s["c"],3)
        self.assertEqual(s["aa"],4)
        self.assertFalse("d" in s)
        with self.assertRaises(KeyError):
            s["d"]  

        s["aa"] = 5
        self.assertEqual(len(s),4)
        self.assertTrue("a" in s)
        self.assertTrue("b" in s)
        self.assertTrue("c" in s)
        self.assertTrue("aa" in s)
        self.assertEqual(s["a"],1)
        self.assertEqual(s["b"],2)
        self.assertEqual(s["c"],3)
        self.assertEqual(s["aa"],5)

        s.clear()
        self.assertEqual(len(s),0)
        self.assertFalse("a" in s)
        self.assertFalse("b" in s)
        self.assertFalse("c" in s)
        self.assertFalse("aa" in s)

    def test_iter(self):
        s = SkipList()
        s["a"] = 1
        s["b"] = 2
        s["c"] = 3
        s["aa"] = 4

        self.assertEqual([ (k,s[k]) for k in s ], [("a",1),("aa",4),("b",2),("c",3)])

    def test_pop(self):
        s = SkipList()
        s["b"] = 1
        s["c"] = 2
        s["bb"] = 3
        s["cc"] = 4
        s["a"] = 5

        self.assertEqual(len(s),5)
        self.assertEqual([ (k,s[k]) for k in s ], [("a",5),("b",1),("bb",3),("c",2),("cc",4)])

        with self.assertRaises(KeyError):
            s.pop("x")

        s.pop("b")
        self.assertEqual(len(s),4)
        with self.assertRaises(KeyError):
            s.pop("b")

        s.pop("a")
        self.assertFalse("a" in s)

        s.pop("bb")
        s.pop("c")
        s.pop("cc")
        self.assertEqual(len(s),0)
        self.assertEqual([ (k,s[k]) for k in s ], [])


