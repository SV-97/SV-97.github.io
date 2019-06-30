---
layout: default
title: SV-97's Webthingy
mathjax: true
---

# Human Resource Machine *XASM*

###### 10.06.19

Ok, so I came across a game called Human Resource Machine last week and blasted through it fairly quickly (I can only recommend it). The game basically is programming a sort of graphical assembly and the sole reason I'm writing about it here is: it supports importing and exporting and exporting source code.

## Instruction set

The HRM asm has a register based instruction set with only ten instructions:

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

## Features of *XASM*

My extended asm (I dubbed it *XASM*) has a new language feature that allows defining the available amount of memory. You then can easily use variables or essentially named registers without having to worry about their actual adresses - they're distributed automatically. I didn't add any new instructions because that would kinda take the fun out of the game.  

## Implementation

[When it got to implementing the whole thing](https://github.com/SV-97/HumanResourceMachine) I started by writing it in Python which worked great. But when I already had the tokenizer etc. I thought that I might as well think of a bytecode, compile the whole thing and build a VM for it. I started doing this in python but then decided to switch over to Rust which seems to be so much nicer when it comes to building language applications (though I think the new walrus operator coming with Python 3.8 will bring some remedy in that domain). I implemented the following architecture:  

![Architecture](https://raw.githubusercontent.com/SV-97/HumanResourceMachine/master/architecture.png)  

It overall was a fairly straightforward process - I stumbled a bit over the pointers but I had to use 16-bit numbers anyway (With 8-bit jumps - I don't think anyone will create programs that are over 255 instructions long) for the operands, so I just used one bit of those for the pointer.  

I mapped the original instructions 1:1 to bytecode and wrote a register machine to execute the whole thing.  
Because I wanted to be able to have some color in the output I also implemented a "logging" system with a *colored!*-macro that allows applying most of the ANSI-codes to format strings and is also easily extendable via a trait if I did miss something.  
Overall this was a really fun project and great exercise in using Rust - I'm kinda tempted to reimplement it in C or more likely C++, just to see how much more of a pain that would be, but I don't think I'll actually do that.  

---
---
