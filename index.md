---
layout: default
title: SV-97's Webthingy
mathjax: true
---

# The coin change problem

###### 23.06.19

The [change-making problem](https://en.wikipedia.org/wiki/Change-making_problem) is a classic problem, where the goal is to divide an amount of money evenly into coins. We'll use this problem to show off different programming paradigms/styles. We'll imagine a vending machine that can take in coins until a treshold value (the price of the item a user bought) is reached - we then give him the change back as a set of coins.

## The foundation

We'll start by defining our foundation - the fronend of our hypothetical vending machine. So we define a list of integers to be our cash register. We'll just use integer-valued coins (so a 1€ coin is a 100ct coin for us) to avoid having to deal with floating point and the errors associated. So our cash register has all the coins from 0.1€ to 2€ to generate change from.
We also define a function that converts our integer values to float strings for us - as well as the price a user has to pay. We'll just hardcode the price to be 2€ to keep it simple for this example. Also as a sidenote: With the current setup of the cash register we have to make the prices so that they can be "built" from coins - we can't give back 0.05€ or something like that (adding a 0.01€ coin would solve that).

```python
def monetary_value(x):
    return f"{x/100:.2f}€"


cash_register = [10, 20, 50, 100, 200]
price = 200
```

The algorithm to take in coins from the customer is fairly straight forward. We just take in coins until the paid amount is ⩾ the price, reject coins that aren't in our cash register as well as non integer values.

```python
paid = 0
while paid < price:
    print(f"You still have to pay {monetary_value(price - paid)}")
    coin = None
    while coin not in cash_register:
        try:
            coin = int(input("Insert a coin: "))
        except ValueError:
            print("Invalid coin")
    paid += coin
```

We then print whatever values we got.

```python
print(f"You had to pay {monetary_value(price)}")
print(f"You paid {monetary_value(paid)}")
```

At this point we're ready to start making change.
For the sake of consistency we'll assume that our customer always put in 1€, 0.2€, 0.1€, 2€ in this order. This will give us an amount of 1.3€ we'll have to turn into cash.

## Iterative

We'll start with the simplest/most straight forward way (to most people) to solve this: An iterative approach

```python
def iterative(paid):
    out_coins = []
    for coin in sorted(cash_register, reverse=True):
        while (paid - price) - coin >= 0:
            out_coins.append(coin)
            paid -= coin
        if paid - price == 0:
            return out_coins
```

We start with making an empty list. We then assert that our cash_register is sorted and reverse it - so that it looks like `[200, 100, 50, ..]`. We then look at each coin value and take coins of that value as long as the difference of the value and the difference between what the customer paid and what the actual price was is bigger or equal to zero. Every time we take a coin we subtract it from the paid value because it's essentially the same as if the customer has paid one less of those coins. The `if` just makes us return early if we already have all the change we need.

## Recursive

Another way to solve this problem is via recursion (though this solution isn't a purely recursive one - we'll get to that at the end). We start with having a `rec_caller` function that just creates a uniform interface with the other functions. It also sorts our global cash register so that we don't sort it in each step of the recursion later on.

```python
def rec_caller(paid):
    global cash_register
    cr = cash_register[:]
    cash_register.sort(reverse=True)
    val = recursive(paid - price)
    cash_register = cr
    return val
```

Then we have our actual function:

```python
def recursive(diff):
    for coin in cash_register:
        if diff - coin >= 0:
            lst = [coin]
            lst.extend(recursive(diff - coin))
            return lst
    return []
```

We recursively build a list of all the coins that are less than or equal to the difference we still have to cover. This actually looks kinda clunky in my opinion - with Python 3.8 we'll be able to write this in a way terser manner.

```python
def recursive(diff):
    for coin in cash_register:
        if (d := diff - coin) >= 0:
            (lst := [coin]).extend(recursive(d))
            return lst
    return []
```

That's fine and works, however there still is a major inefficiency in this code: we check every coin every time - even if we know it can't possibly be chosen.
So we'll modify the code to improve on that:

```python
def rec_caller(paid):
    global cash_register
    coins = iter(sorted(cash_register, reverse=True))
    val = recursive(paid - price, coins)
    return val

def recursive(diff, coins):
    coin_filter = []
    for coin in coins:
        if diff - coin >= 0:
            lst = [coin]
            lst.extend(recursive(diff - coin, filter(lambda x: x not in coin_filter, coins)))
            return lst
        coin_filter.append(coin)
    return []
```

We now check if a coin can be used - and if it can't we add it to our filter. This filter then filters out all coins that didn't fit at some point.

## The wonky way

We'll do a combo of iterative/functional next. This was just the first solution I came up with and I thought it was somewhat elegant (though massively inefficient I think) so I included it.

```python
def func_it(paid):
    out_coins = []
    while paid > price:
        out_coin = min(
            filter(
                lambda pair: pair[0] >= 0,
                map(lambda coin: ((paid - price) - coin, coin), cash_register)
                ),
            key=lambda m: m[0])[1]
        out_coins.append(out_coin)
        paid -= out_coin
    return out_coins
```
We again start out with an empty list to hold the change we give out. We then iterate as long as our paid value is bigger than our price - so as long as we have a nonzero difference.
Then it gets a bit messy. Let's go through this one by one:

* `map(lambda coin: ((paid - price) - coin, coin), cash_register)` We start off by mapping a function to our cash register. This function calculates the difference between how much the customer has paid to much and every coin in the cash register and then packages this difference into a tuple together with the corresponding coin value. We'll call this `map_` in the following snippet.
* `filter(lambda pair: pair[0] >= 0, map_)` We now filter out all of the pairs, for which the `0`th value is less than 0. So all the coins that would be too big. Lets call this stage `filter_`
* `min(filter_, key: lambda m: m[0])` we now take the pair with the smallest difference from our iterator.
* `min_[1]` and take the first elementh from it which is our coin.

Then we just append the coin, subtract it for the next step and move on.


## Purely Functional

Now the last way I'll cover is doing it functionally. This is last because it requires us to have a different interface as the other functions because we can't have a global cash register (or else it wouldn't be pure) (we could use an interface method theoretically though). This is also a fully recursive way of solving this problem. Ok here we go:

### Python

```python
def functional(cash_register, amount):
    if amount == 0: return []
    if len(cash_register) == 0: return []
    c, *r = cash_register
    if amount - c >= 0:
        return [c, *functional(cash_register, amount - c)]
    else:
        return functional(r, amount)
```

### Haskell

```haskell
getChange :: [Int] -> Int -> [Int]
getChange _ 0 = []
getChange [] _ = []
getChange (c: r) amount = 
    if amount - c >= 0
        then c: (getChange (c:r) (amount - c))
        else getChange r amount

```

Just to clarify: this is the same code - once written in Python and once in Haskell. The Haskell one allows us to do a bit of fancy stuff but we'll get to that.
The first line is a function definition in both cases. The second one handles the case that the amount of money is 0. If we don't have anything to generate change for we of course give back an empty list. Same thing if we don't have anything in our cash register: we can't possibly give anything back, so the empty list it is.
Then it gets a bit more interesting. We start off by decomposing our cash register into its *head* (the biggest coin in the register) and it's *tail* (the rest). In the Haskell example we also bind the lone integer we passed in to the name `amount`.
We then determine if the current coin is a valid choice. If it is we say "build a list with the current coin as the first element, the rest of the list should be whatever is in this other list" where the other list is a call to `getChange` with the full cash register and an reduced amount of money.
If the current coin isn't a fit we drop it from the list of possible values by calling `getChange` with only the tail of our list.

The two functions are basically identical - except that the Haskell one allows us to use **currying**. Currying is the process of taking a function like $f(a,b)$ and making it a composition like $g(a)(b)$ where $g(a)$ is a function in itself. So it converts a multiargument function into a function with one less argument. This allows us to do stuff like the following:

```haskell
*Main> getChange [200, 100, 50, 20, 10, 1] 130
[100,20,10]
*Main> f = getChange [200, 100, 50, 20, 10, 1]
*Main> f 130
[100,20,10]
*Main> f 150
[100,50]
```

---
---

# UTF-8

###### 21.06.19

Ok, so I've guest authored on a blog ([pylenin](https://www.pylenin.com/blogs/python-comparison-operators/)) recently and thought I might as well share what I've written up here.
The original blog was on comparison operators in python and how comparison based on ASCII works - My contribution is on UTF-8/why and ASCII explanation still holds for the most part.

## Excerpt from pylenin

### Enter: UTF-8

The thing is... Python doesn't actually use ASCII - most systems don't. But the explanations given above still hold true for the most part.
Now Python doesn't actually use ASCII (at least since Python 3 came out - Python 2 *did* use ASCII), but rather another encoding called **UTF-8** where UTF stands for **UCS Transformation Format** and UCS stands for **Universal Coded Character Set**. UTF-8 is what is called a **variable width encoding** and the de facto standard when it comes to **Unicode**. The beauty of UTF-8 is that it supports loads of special characters - but not at the price of making the regularly used characters (for the western world at least) need more memory. This is the *variable width* part mentioned earlier. 

#### The gritty details

If we take a look at the most common characters used, their memory representation looks like this:

```rust
'R' => 0b0101_0010 <U+0052>
's' => 0b0111_0011 <U+0073>
```

The part in angled brackets is called a **unicode code point**. It's usually written in hex - as it is here. If you compare these values to their ASCII pendant, you'll see that they're actually the same. This is another great property of UTF-8 - it's backwards compatible with ASCII and also the reason, why the above explanation still holds true for the most part. 
The code points up to `U+007F` are encoded in on byte of data with every codepoint starting with a `0`. This means there are 7 bits to represent all the ASCII symbols. If you go higher than that, you'll have a header byte that always starts with `11` and additional data bytes that start with `10`. 
Let's for example take Unicode code point `U+2705` (Called `:white_check_mark:`, it's the ✅ emoji). We get the binary represantation `0b1110_0010_1001_1100_1000_0101`, which in hex is `0xe29c85`. We can see that it's a three byte code point and can also see the initial `11` and following `10`s. UTF-8 may encode codepoints with up to 4 bytes. 

#### Potential pitfalls

So this is all fair and well and feels like it's just ASCII with more characters - the thing is, it isn't. Becaus a unicode *character* may actually consist of multiple *codepoints*. A good example for this are for example the flag emojis which consist of **regional indicator symbols**. The flag of peru for example consists of the codepoints `U+1F1F5` and `U+1F1EA`. It's two codepoints that, if the target system supports it, are rendered as a single character.
So in the end unicode and UTF-8 are fairly complicated topics - but you rarely need all this extra information, because if you just want to sort something alphabetically, you'll most likely deal with the basic ASCII character set. 

#### A bit of insider knowledge

Should you ever need the ASCII letters or something similar in your code - don't hardcode them in please. They're all available in the standardlibrary's [`string` module](https://docs.python.org/3/library/string.html).
```python3
>>> from pprint import pprint
>>> import string
>>> pprint(list(filter(lambda name: not name.startswith("_"), dir(string))))
['Formatter',
 'Template',
 'ascii_letters',
 'ascii_lowercase',
 'ascii_uppercase',
 'capwords',
 'digits',
 'hexdigits',
 'octdigits',
 'printable',
 'punctuation',
 'whitespace']
```

#### Resources
* [Python docs on comparisons of sequences](https://docs.python.org/3/tutorial/datastructures.html#comparing-sequences-and-other-types)
* [Python docs on unicode](https://docs.python.org/3/howto/unicode.html)
* [Wikipedia Article on UTF-8](https://en.wikipedia.org/wiki/UTF-8)
* [Wikipedia Article on variable width encoding](https://en.wikipedia.org/wiki/Variable-width_encoding)
* [Great talk on emoji/unicode in German](https://youtu.be/73VEB2zr4HU)
* [Computerphile video on unicode](https://youtu.be/MijmeoH9LT4)

---
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

# McCulloch/Pitts neuron model

###### 26.05.19

So I came across the McCulloch/Pitts (I'll just call it Mcp) neuron model while reading on ANNs today. The Mcp is a comparatively easy model that doesn't have a concept of weights. The neurons are of a binary nature. They fire if the sum of their inputs exceed a treshold value (called S in the following). They also have inhibitor inputs that prevent the neuron from firing completely if they're present.
Naturally I chose to [implement it in python](https://github.com/SV-97/Py3-Private/tree/master/P3_060_NeuroComputingBasics) and play around with it.

## Basic logic

I started off with creating AND and OR gates from the neurons which worked great.

|                         AND-Gate |                        OR-Gate |
|:--------------------------------:|:------------------------------:|
| ![AND-Gate](./media/mcp_and.png) | ![OR-Gate](./media/mcp_or.png) |

I just connected normal inputs to the node's inputs, and negated ones to the inhibition. This fails because that way the treshold value isn't reached and it can't possibly fire with the inhibitor being > 0.
While it took me some time to figure this out I was able to quickly adapt to it and create a few more complex gates after I did.

|                        XOR-Gate |                          NAND-Gate |
|:-------------------------------:|:----------------------------------:|
|![XOR-Gate](./media/mcp_xor.png) | ![NAND-Gate](./media/mcp_nand.png) |

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

![Two-Bit-Half-Adder](./media/mcp_adder.png)

---
---

# Other stuff

* [CAD Services](https://sites.google.com/view/sv-cad/) - Where I post everything regarding my CAD work.
* [Book index](./books.md) - Books I'm currently reading, have already finished, on backlog etc. you get the notion.
* [About me](./about.md)
  
---
