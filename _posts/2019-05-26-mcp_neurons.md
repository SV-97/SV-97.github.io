---
layout: single
title: McCulloch/Pitts neuron model
#mathjax: true
categories: soft-computing math CS languages
---

So I came across the McCulloch/Pitts (I'll just call it Mcp) neuron model while reading on ANNs today. The Mcp is a comparatively easy model that doesn't have a concept of weights. The neurons are of a binary nature. They fire if the sum of their inputs exceed a treshold value (called S in the following). They also have inhibitor inputs that prevent the neuron from firing completely if they're present.
Naturally I chose to [implement it in python](https://github.com/SV-97/Py3-Private/tree/master/P3_060_NeuroComputingBasics) and play around with it.

## Basic logic

I started off with creating AND and OR gates from the neurons which worked great.

|                         AND-Gate |                        OR-Gate |
|:--------------------------------:|:------------------------------:|
| ![AND-Gate](/assets/images/2019-05-26-mcp_neurons/mcp_and.png) | ![OR-Gate](/assets/images/2019-05-26-mcp_neurons/mcp_or.png) |

I just connected normal inputs to the node's inputs, and negated ones to the inhibition. This fails because that way the treshold value isn't reached and it can't possibly fire with the inhibitor being > 0.
While it took me some time to figure this out I was able to quickly adapt to it and create a few more complex gates after I did.

|                        XOR-Gate |                          NAND-Gate |
|:-------------------------------:|:----------------------------------:|
|![XOR-Gate](/assets/images/2019-05-26-mcp_neurons/mcp_xor.png) | ![NAND-Gate](/assets/images/2019-05-26-mcp_neurons/mcp_nand.png) |

## Modelling DSL

After I was done playing around with it I thought that this was a bit short of an "exploration" and constructing the nets by hand like this was too big of a hassle and decided to write a small DSL to automate it.
The language looks like this

```desc
title: XOR-Gate using McCulloch-Pitts-Neurons 
in: a b 
out: X 
c: 1 
d: 1 
e: 1 
a -- c 
b -o c 
a -o d 
b -- d 
d -- e 
c -- e 
e -- X
```

Which of course is fairly minimalistic but enough for what I wanted to do here. It also transpiles to graphviz-dot to generate these graphs I've had in here. The language essentially comes down to declaring inputs with "in:", outputs with "out:", internal neurons with their name followed by their treshold and connections with  "--" for regular links and "-o" for inhibitions.
I've also tried using regular expressions for parsing which was a first but worked out fairly well ( even though the code isn't exactly beautiful ).

Just for the fun of it I also built a two bit half-adder using these neurons and I haven't tested it yet, but I think it works (In case anyone is interested: it took about 50 lines of my descriptor-code).

## Two-Bit-Half-Adder

![Two-Bit-Half-Adder](/assets/images/2019-05-26-mcp_neurons/mcp_adder.png)
