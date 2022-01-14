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

# Software Used
- <b> Python language</b> 

- <b> Snap.py (SNAP for Python) </b>: Stanford Network Analysis Platform (SNAP) is a general purpose network analysis and graph mining library. It efficiently manipulates large graphs, calculates structural properties, generates regular and random graphs, and supports attributes on nodes and edges. For details [https://snap.stanford.edu/index.html](https://snap.stanford.edu/index.html)

# Datasets


# Implementation

## Init

## Ecc

# How to execute

## requirements

## datasets download

# Computational Complexity

# Results Discussion

## edge filtering based on propability
- before/after filtering for each probability distribution function used

- tests configuration on paper

# Conclusions


Data una threshold function t:V -> {0,1,2,…}
- t(v) = numero di adiacenti attivi del nodo v necessari ad attivare v
- quale treshold function prendiamo in considerazione?
    - COSTANTE
    - A MAGGIORANZA
    - PROPORZIONALE AL GRADO


Data una distribuzione di probabilità associata agli archi di G p:E -> [0,1]
- p(u,v) = probabilità con cui un nodo attivo u influenza un suo adiacente v


1. Assegniamo a ciascun arco del grafo una probabilità (valore compreso tra 0 e 1)

2. Applichiamo il principio di decisione differita: per ogni arco del grafo viene generato un numero pseudocasuale compreso tra 0 e 1; se il numero generato è minore della probabilità presente sull'arco, l'arco viene rimosso. In altre parole rimuoviamo gli archi tra nodi che infettano con una probabilità minore rispetto a quella richiesta. Calcoliamo il sottografo risultante.

3. Inizializziamo i tresholds associati ai nodi in base alla funzione di treshold utilizzata.

4. Il grafo così calcolato e i tresholds vengono dati in input all'algoritmo di Target Set Selection (TSS) che calcola l'insieme soluzione e lo restituisce in output. Questa procedura viene iterata per 10 volte e poi viene calcolata la media della grandezza dell'insieme soluzione.