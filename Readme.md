# Counterfactual Regret Minimization

## By Judah Goldfeder

## Overview

This repo serves as a didactic example of Counterfactual Regret Minimization in action. the CFR algorithm is used to find a nash equilibrium in 2 player zero sum imperfect information games. 

The game that was used in this example is Kuhn Poker. Kuhn Poker has a long history in game theory literature, and has well known theoretical results, which makes it easy to verify that the code works. For more information on Kuhn Poker, see [here](https://en.wikipedia.org/wiki/Kuhn_poker).

The details of CFR, and a description of how it applies to Kuhn Poker, were adopted from this [very excellent paper](http://modelai.gettysburg.edu/2013/cfr/cfr.pdf), although all the code is original.

## Implementation
This repo contains two seperate algorithms that converge to a Nash Equilibrium. The first algorithm considers a modifed version of Kuhn Poker in normal form. The normal form version is of course strategically identical to the standard sequential form, but allows us to calculate a Nash Equilibrium with simple regret matching. The second algorithm considers the standard version of Kuhn Poker, and finds a Nash  Equilibrium using the CFR algorithm.

## Theoretical Correctness
It is a well known [theoretical result](https://poker.cs.ualberta.ca/publications/AAAI05.pdf) that in an equilibrium strategy, player one has an expected value of -1/18 per hand (or about -.055). In a small number of iterations, both the normal form and sequential form algorithms converge to this value, confirming the correctness of the implementation

## Running The Code
To run the code, invoke one of:

> python normal_form.py <num_iterations>

> python sequential_form.py  <num_iterations>

