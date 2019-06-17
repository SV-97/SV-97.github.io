---
layout: default
---

# Human Resource Machine *XASM*

**10.06.19**

Ok, so I came across a game called Human Resource Machine last week and blasted through it fairly quickly (I can only recommend it). The game basically is programming a sort of graphical assembly and the sole reason I'm writing about it here is: it supports importing and exporting and exporting source code. The HRM asm has a register based instruction set with only ten instructions:

* **Inbox**: Fetch a new input block (an int between -999 and 999 or a char) from the input stream
* **Outbox**: Write your current accumulator to the output stream
* **Copyfrom** rs: Copy to the accumulator from register rs
* **Copyto** rd: Copy the accumulator to register rd
* **Add** rs: Add rs to the accu
* **Sub** rs: Subtract rs from the accu
* **Bumpup** rd: Increment rd and load to accu
* **Bumpdn** rd: Decrement rd and load to accu
* **Jump** m: Jump to m
* **Jumpz** m: Jump to m if accu is zero
* **Jumpn** m: Jump to m if accu is less than zero

and also supports pointers (surrrounding a register with brackets makes it a pointer) and single line comments.
Now this is great, but I kinda wanted to do more complicated stuff/ do complicated stuff more easily... so naturally I wrote my own language that offers just slightly more abstraction over HRM's vanilla language and compiles to native HRM ASM.
My extended asm (I dubbed it *XASM*) has a new language feature that allows defining the available amount of memory. You then can easily use variables or essentially named registers without having to worry about their actual adresses - they're distributed automatically. I didn't add any new instructions because that would kinda take the fun out of the game.  

[When it got to implementing the whole thing](https://github.com/SV-97/HumanResourceMachine) I started by writing it in Python which worked great. But when I already had the tokenizer etc. I thought that I might as well think of a bytecode, compile the whole thing and build a VM for it. I started doing this in python but then decided to switch over to Rust which seems to be so much nicer when it comes to building language applications (though I think the new walrus operator coming with Python 3.8 will bring some remedy in that domain). I implemented the following architecture:  

![Architecture](https://raw.githubusercontent.com/SV-97/HumanResourceMachine/master/architecture.png)  

It overall was a fairly straightforward process - I stumbled a bit over the pointers but I had to use 16-bit numbers anyway (With 8-bit jumps - I don't think anyone will create programs that are over 255 instructions long) for the operands, so I just used one bit of those for the pointer.  

I mapped the original instructions 1:1 to bytecode and wrote a register machine to execute the whole thing.  
Because I wanted to be able to have some color in the output I also implemented a "logging" system with a *colored!*-macro that allows applying most of the ANSI-codes to format strings and is also easily extendable via a trait if I did miss something.  
Overall this was a really fun project and great exercise in using Rust - I'm kinda tempted to reimplement it in C or more likely C++, just to see how much more of a pain that would be, but I don't think I'll actually do that.  

# McCulloch/Pitts neuron model

**26.05.19**

So I came across the McCulloch/Pitts (I'll just call it Mcp) neuron model while reading on ANNs today. The Mcp is a comparatively easy model that doesn't have a concept of weights. The neurons are of a binary nature. They fire if the sum of their inputs exceed a treshold value (called S in the following). They also have inhibitor inputs that prevent the neuron from firing completely if they're present.
Naturally I chose to [implement it in python](https://github.com/SV-97/Py3-Private/tree/master/P3_060_NeuroComputingBasics) and play around with it.
I started off with creating AND and OR gates from the neurons which worked great.

|                         AND-Gate |                        OR-Gate |
|:--------------------------------:|:------------------------------:|
| ![AND-Gate](./media/mcp_and.png) | ![OR-Gate](./media/mcp_or.png) |

I just connected normal inputs to the node's inputs, and negated ones to the inhibition. This fails because that way the treshold value isn't reached and it can't possibly fire with the inhibitor being > 0.
While it took me some time to figure this out I was able to quickly adapt to it and create a few more complex gates after I did.

|                        XOR-Gate |                          NAND-Gate |
|:-------------------------------:|:----------------------------------:|
|![XOR-Gate](./media/mcp_xor.png) | ![NAND-Gate](./media/mcp_nand.png) |

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

![Two-Bit-Half-Adder](./media/mcp_adder.png)

# Other stuff

* [CAD Services](https://sites.google.com/view/sv-cad/) - Where I post everything regarding my CAD work.
* [Book index](./books.md) - Books I'm currently reading, have already finished, on backlog etc. you get the notion.
* [About me](./about.md)