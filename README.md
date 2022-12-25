# Challenging algorithms and data structures every programmer should try

This is a personal exercise following the recmmendation from Austin Z. Henley in [Challenging algorithms and data structures every programmer should try](https://austinhenley.com/blog/challengingalgorithms.html).

## Topological Sort

Imagine that you have a series of steps that depend on each other and you have to establish an order of execution that maintains the dependencies. For a given graph of dependencies, there could be zero, one, or multiple solutions.

For example, if A depends on B and B on A, there is no solution. If A depends on B, there is onl one solution and if C depends on A and B, there are two solutions.

The input of the problem is a Directed Graph and the problem has solution if there are no cycles in the graph.

see [wikipedia article](https://en.wikipedia.org/wiki/Topological_sorting).