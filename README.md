<p align="center">
  <h2 align="center">Target Set Selection on Social Networks</h2>
    <br>
  <p align="center">
    <b>Nicola De Cristofaro - 0522500876</b><br>
    Social Networks course project <br>
	  Department of Computer Science, Master's Degree, Cloud Computing curriculum <br>
	  University of Salerno <br>
    Email: n.decristofaro2@studenti.unisa.it  
  </p>
</p>

# Problem Description
The phenomenon of social influence has been extensively studied as it can bring benefits in different contexts. Social Influence is the process by which individuals adjust their opinions, revise their belief, or change their behaviours as a result of interactions with other people. In particular, this process has gained a lot of interest from advertisers to exploit "viral marketing" namely the spread of information about products and their adoption by people.

In the context of viral marketing, the problem could be stated as follow: 
- given a social network, find a small number of individuals **(Target Set)**, who when convinced about a new product will influence others by word-of-mouth, leading to a large number of adoptions of the product.

This small number of individuals that constitutes the target set are called **seeds**, individuals who are expected to use their social network position or personal influence to trigger cascades of product adoption.

**Our problem is to minimize the number of seeds, in other words we want to find the minimum target set for which we will be able to influence the entire network.**

# Formalization of the problem
**Instance:**
- Given G = (V,E) a graph that models the network
- Given the function <img src="https://latex.codecogs.com/svg.image?t&space;:&space;V&space;\rightarrow&space;\mathbb{N}_{0}&space;=&space;\left\{&space;0,1,...&space;\right\}" title="t : V \rightarrow \mathbb{N}_{0} = \left\{ 0,1,... \right\}" /> assigning **tresholds** to the vertices of G. 
   
   *What do the thresholds represent?* For each node v ∈ V, the value **t(v)** quantifies how hard it is to influence node v, in the sense that easy-to-influence nodes of the network have “low” threshold values, and hard-to-influence nodes have “high” threshold values.

**Problem:**
*Find a target set S ⊆ V of minimum size for G*
Dato un grafo non direzionato G=(V,E)

**Extra Requirement:**
Instead of considering all the edges of the graph that models the network, we want to consider a subset of them. How? Let us consider a probability distribution associated with the edges of our graph G.
<img src="https://latex.codecogs.com/svg.image?\bg_white&space;p:E&space;\rightarrow&space;&space;[0,1]" title="\bg_white p:E \rightarrow [0,1]" /> where **p(u,v) = probability with which an active node u influences its neighbor v.**

We apply the principle of deferred decision: for each edge of the graph a pseudorandom number between 0 and 1 is generated. If the generated number is less than the probability present on the edge (i.e. the node infects with a probability lower than the required one), the edge is removed from the graph.

# Software Used
- <b> Python language</b> 

- <b> Snap.py (SNAP for Python) </b>: Stanford Network Analysis Platform (SNAP) is a general purpose network analysis and graph mining library. It efficiently manipulates large graphs, calculates structural properties, generates regular and random graphs, and supports attributes on nodes and edges. For details [https://snap.stanford.edu/index.html](https://snap.stanford.edu/index.html)

# Implementation

## Init

## Ecc

# How to execute

## requirements

# Computational Complexity

# Datasets
To carry out the tests on the implemented algorithm, the datasets provided by SNAP were used ([https://snap.stanford.edu/data/index.html](https://snap.stanford.edu/data/index.html)). In particular, in the "Social Networks" category where the edges represent interactions between people.

The following datasets were used:
- **musae-twitch:** in this dataset nodes are the users of Twitch Social Network and the links are mutual friendships between them. These social networks data were collected in May 2018 and they are organized depending on the language used by users (we consider the ENG variant).
- **musae-facebook:** in this dataset nodes represent official Facebook pages while the links are mutual likes between sites. 

Here are some statistics on the datasets used:

| Dataset Name   	| #nodes 	| #edges 	| Max Node Degree 	| Avg Node Degree 	| Clustering Coefficient 	| Website link for download                                            	|
|----------------	|--------	|--------	|-----------------	|-----------------	|------------------------	|----------------------------------------------------------------------	|
| musae-twitch   	| 7126   	| 35324  	| 720             	| 10              	| 0.13092821901472068    	| https://snap.stanford.edu/data/twitch-social-networks.html           	|
| musae-facebook 	| 22470  	| 171002 	| 709             	| 16              	| 0.36247953821665585    	| https://snap.stanford.edu/data/facebook-large-page-page-network.html 	|

# Tests execution and results discussion

## edge filtering based on propability
- test configuration
- before/after filtering for each probability distribution function used

## TSS executions
- tests configuration, execution and discussion on graphics

# Conclusions


4. Il grafo così calcolato e i tresholds vengono dati in input all'algoritmo di Target Set Selection (TSS) che calcola l'insieme soluzione e lo restituisce in output. Questa procedura viene iterata per 10 volte e poi viene calcolata la media della grandezza dell'insieme soluzione.