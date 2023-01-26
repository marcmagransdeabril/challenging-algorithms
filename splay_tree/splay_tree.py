import unittest
import random


class Node:
    def __init__(self,key,value):
        self.key=key
        self.value=value
        self.left=None
        self.right=None

    def __str__(self):
        return "({},{},{},{})".format(self.key,self.value,str(self.left),str(self.right))


class SplayTree:
    

    def __init__(self):
        self.root = None
        self.len=0
        self.iter_stack=[]

    def __right_rotate(self,x):
        if not x.left:
            #if not possible return the same
            return x

        y = x.left;
        x.left = y.right
        y.right = x
        return y

    def __left_rotate(self,x):
        if not x.right:
            return x

        y = x.right 
        x.right = y.left 
        y.left = x
        return y

    def __splay(self,root,key):
        if not root or root.key == key:
            return root

        if root.key > key:
            # left
            if not root.left:
                return root

            if root.left.key > key:
                # left-left
                # Move the ket to root.left.left

                root.left.left = self.__splay(root.left.left,key)
                root = self.__right_rotate(root)

            elif root.left.key < key:
                # left-right
                
                root.left.right = self.__splay(root.left.right,key)
                root.left = self.__left_rotate(root.left)

            x = self.__right_rotate(root) 

            return x

        else:
            # right
            if not root.right:
                return root

            if root.right.key > key:
                # right-right

                root.right.left = self.__splay(root.right.left,key)
                root.right = self.__right_rotate(root.right)

            elif root.right.key < key:
                # right-left

                root.right.right = self.__splay(root.right.right,key)
                root = self.__left_rotate(root)

            x = self.__left_rotate(root) 

            return x



    def __setitem__(self, searchKey, value):
        if not self.root:
            self.root = Node(searchKey,value)
            self.len += 1
            return

        self.root = self.__splay(self.root,searchKey)

        if self.root.key == searchKey:
            self.root.value = value
            return

        node = Node(searchKey,value) 

        if self.root.key > searchKey:
            node.right = self.root
            if self.root.left and self.root.left.key < searchKey:
                node.left = self.root.left
                self.root.left = None
        else:
            node.left = self.root
            if self.root.right and self.root.right.key > searchKey:
                node.right = self.root.right
                self.root.right = None

        self.root = node

        self.len += 1

    def __contains__(self,key):
        self.root = self.__splay(self.root,key)

        return self.root is not None and self.root.key == key

    def __iter__(self):
        q = []
        self.iter_stack=[]

        curr  = self.root
        while curr:
            q.append(curr)
            curr = curr.left

        while q:
            node = q.pop(-1)
            self.iter_stack.append(node.key)

            curr = node.right
            while curr:
                q.append(curr)
                curr = curr.left

        return self

    def __next__(self):
        
        if not self.iter_stack:
            raise StopIteration()

        return self.iter_stack.pop(0)

 

    def __len__(self):
        return self.len


    def __getitem__(self, searchKey):
        self.root = self.__splay(self.root,searchKey)

        if self.root is None or self.root.key != searchKey:
            raise KeyError("key '{}' not found".format(searchKey))

        return self.root.value

    
    def clear(self):
        self.__init__()

    def pop(self, searchKey):
        if not self.root:
            raise KeyError("key '{}' not found".format(searchKey))

        self.root = self.__splay(self.root,searchKey)

        if self.root.key != searchKey:
            raise KeyError("key '{}' not found".format(searchKey))


        if not self.root.left:
            self.root = self.root.right

        else:
            temp = self.root;
  
            self.root = self.__splay(self.root.left, searchKey)
  
            self.root.right = temp.right;

        self.len -= 1




class Testing(unittest.TestCase):
    def test_skiplist(self):
        s = SplayTree()
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
        s = SplayTree()
        s["a"] = 1
        s["b"] = 2
        s["c"] = 3
        s["aa"] = 4

        self.assertEqual([ (k,s[k]) for k in s ], [("a",1),("aa",4),("b",2),("c",3)])

    def test_pop(self):
        s = SplayTree()
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


