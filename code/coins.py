def monetary_value(x):
    return f"{x/100:.2f}€"


cash_register = [10, 20, 50, 100, 200]

price = 200 # 2€ price

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

print(f"You had to pay {monetary_value(price)}")
print(f"You paid {monetary_value(paid)}")


def iterative(paid):
    out_coins = []
    for coin in sorted(cash_register, reverse=True):
        while (paid - price) - coin >= 0:
            out_coins.append(coin)
            paid -= coin
        if paid - price == 0:
            return out_coins


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


def functional(cash_register, amount):
    if amount == 0: return []
    if len(cash_register) == 0: return []
    c, *r = cash_register
    if amount - c >= 0:
        return [c, *functional(cash_register, amount - c)]
    else:
        return functional(r, amount)


out_coins = iterative(paid)
out_coins = func_it(paid)
out_coins = rec_caller(paid)
out_coins = functional(sorted(cash_register, reverse=True), 130)
for coin in out_coins:
    print(monetary_value(coin))