---
layout: single
title: The coin change problem
#mathjax: true
categories: math programming python haskell
published: false
---

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

- `map(lambda coin: ((paid - price) - coin, coin), cash_register)` We start off by mapping a function to our cash register. This function calculates the difference between how much the customer has paid to much and every coin in the cash register and then packages this difference into a tuple together with the corresponding coin value. We'll call this `map_` in the following snippet.
- `filter(lambda pair: pair[0] >= 0, map_)` We now filter out all of the pairs, for which the `0`th value is less than 0. So all the coins that would be too big. Lets call this stage `filter_`
- `min(filter_, key: lambda m: m[0])` we now take the pair with the smallest difference from our iterator.
- `min_[1]` and take the first elementh from it which is our coin.

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
Then it gets a bit more interesting. We start off by decomposing our cash register into its _head_ (the biggest coin in the register) and it's _tail_ (the rest). In the Haskell example we also bind the lone integer we passed in to the name `amount`.
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
