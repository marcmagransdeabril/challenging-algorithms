# Challenging algorithms and data structures every programmer should try

This is a personal exercise following the recmmendation from Austin Z. Henley in [Challenging algorithms and data structures every programmer should try](https://austinhenley.com/blog/challengingalgorithms.html).

## Topological Sort

Imagine that you have a series of steps that depend on each other and you have to establish an order of execution that maintains the dependencies. For a given graph of dependencies, there could be zero, one, or multiple solutions.

For example, if A depends on B and B on A, there is no solution. If A depends on B, there is onl one solution and if C depends on A and B, there are two solutions.

The input of the problem is a Directed Graph and the problem has solution if there are no cycles in the graph.

see [wikipedia article](https://en.wikipedia.org/wiki/Topological_sorting).

## Recursive Descent Parsing

The basic idea is simple, given a grammar, we map each kind of expression to a c

see [wikipedia article](https://en.wikipedia.org/wiki/Recursive_descent_parser)


## Diff

Given two strings, how do we calculae the difference between them. That is, the series of edits required to transform one string into another (i.e. outputs of the diff algorithm)? This problem is the dual of finding a longest common subsequence of two strings.

The implementation in this case is less efficient than the one from Myers, but it is far more easy to understand. 

see [Eugene W. Myers, AnO(ND) difference algorithm and its variations, 1986](https://link.springer.com/article/10.1007/BF01840446)



## Suffix Tree

