---
layout: default
title: SV-97's Webthingy
mathjax: true
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
