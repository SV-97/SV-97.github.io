---
layout: default
title: SV-97's Webthingy
mathjax: true
---

# On the periodicity of the sums of sines

###### 20.06.19

Ok so I've thought about this before because wolfram-alpha for example says that a function like the one in the following plot isn't periodic:  
![Periodicity example](./media/periodicity_example.png)  
Which, just from looking at the plot, seems wrong. Calculating specific values also seems to support that it's a periodic function. So I've set out to prove that they're wrong.
<a href="./media/periodicity.pdf" target="_blank">PDF with proof</a>
If you find anything wrong with the proof please let me know.

**EDIT**: Turns out that wolfram alpha actually seems to do it right but is really picky about how you plug the numbers in.  
For example: Take $$\sin(8.5 \cdot 2 \pi x) + \sin(17 \cdot 2 \pi x)$$.
Plugging this in as [`period of sin(8.5*2*pi*x) + sin(17*2*pi*x)`](https://www.wolframalpha.com/input/?i=period+of+sin(8.5*2*pi*x)+%2B+sin(17*2*pi*x)) leads WA to say that it's not periodic. It however thinks differently when you plug the exact same thing in as [`period of sin(17*pi*x) + sin(34*pi*x)`](https://www.wolframalpha.com/input/?i=period+of+sin(17*pi*x)+%2B+sin(34*pi*x)). It now says that it's periodic in $\frac{2}{17}$. Using the methods from my proof we get $\frac{1}{8.5}$ which of course is the exact same thing.  
But if we go ahead and add decimal points to the numbers in our WA formula like this [`period of sin(17.0*pi*x) + sin(34.0*pi*x)`](https://www.wolframalpha.com/input/?i=period+of+sin(17.0*pi*x)+%2B+sin(34.0*pi*x)) WA is back to thinking that it's not a periodic function. This probably comes down to it not going symbolically here but rather using floating point arithmetic. We can also see this at work when comparing [`plot sin(17*pi*x) - sin(2*8.5*pi*x)`](https://www.wolframalpha.com/input/?i=plot+sin(17*pi*x)+-+sin(2*8.5*pi*x)) and [`plot sin(17.0*pi*x) - sin(2*8.5*pi*x)`](https://www.wolframalpha.com/input/?i=plot+sin(17.0*pi*x)+-+sin(2*8.5*pi*x)). One of them gives the expected plot - the other one however...gives just about zero but with bumps every now and then. Just goes to show that you should always consider the capabilities of the systems you're using.

---
---
