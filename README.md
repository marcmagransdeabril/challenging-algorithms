# Challenging algorithms and data structures every programmer should try

This is a personal exercise following the recmmendation from Austin Z. Henley in [Challenging algorithms and data structures every programmer should try](https://austinhenley.com/blog/challengingalgorithms.html).

## Topological Sort

Imagine that you have a series of steps that depend on each other and you have to establish an order of execution that maintains the dependencies. For a given graph of dependencies, there could be zero, one, or multiple solutions.

For example, if A depends on B and B on A, there is no solution. If A depends on B, there is onl one solution and if C depends on A and B, there are two solutions.

The input of the problem is a Directed Graph and the problem has solution if there are no cycles in the graph.

see [wikipedia article](https://en.wikipedia.org/wiki/Topological_sorting).

## Diff

Given two strings, how do we calculae the difference between them. That is, the series of edits required to transform one string into another (i.e. outputs of the diff algorithm)? This problem is the dual of finding a longest common subsequence of two strings.

The implementation in this case is less efficient than the one from Myers, but it is far more easy to understand as it does not require changing the coordinates of the indexes. 

see [Eugene W. Myers, AnO(ND) difference algorithm and its variations, 1986](https://link.springer.com/article/10.1007/BF01840446) for the more efficient variant of the diff algorithm.


## Bloom filter

A Bloom Filter is an space efficient probabilitstic set that scales well up to billions of entries. This data structure is used to test whether an element is a member of a set. False positive matches are possible, but false negatives are not. That is, a query returns either "possibly in set" or "definitely not in set".

The false positive rate is determined by the size $n$ of the filter, the number of elements $m$ already added, and the number of hash functions $k$ according to:

$$
( 1 - exp^{-k n / m} )^k
$$

see [wikipedia article](https://en.wikipedia.org/wiki/Bloom_filter).

## Consistent Hashing

Consistent hashing is a special kind of hashing technique such that when a hash table is resized then just a small subset of the kes has to be remapped. 

Consistent hashing is a fundamental building block of modern distributed system to to automate the data partitioning and load balancing in services like Google Maglev, Dynamo DB, Cassandra, Riak, Akkami, etc.

The basic techinque has a cost of inserting and searching the host for a given blob of O(log N). Where N is the number of servers. The cost of inserting or deleting a server if O(log N) + O(M/N). Where M is the total number of Blobs partition between N servers. This basic technique can be further extended by adding a number of aliases per server in order spread the load more evently.

see [wikipedia article](https://en.wikipedia.org/wiki/Consistent_hashing). 

## Skip list

A skip list is a probabilistic data structure that allows expected retrieval, insert, and delete of entries in $O(log(n))$ time and $O(n)$ space with a much simpler implementation that a balanced tree. 

see the original paper from [Pugh, Skip lists: A probabilistic alternative to balanced trees, 1990](ftp://ftp.cs.umd.edu/pub/skipLists/skiplists.pdf) fpr the best explanation of the data structure and its implementation.

## Piece table

## Splay tree




