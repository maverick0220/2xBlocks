bigData = []

ranks = list("abcdfeghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ∞")

value = 1.6384
rank = "a"
for i in range(519):
    bigData.append(f"{int(value)}{rank}")
    value = 2 * value

    if value > 1000:
        value = value / 1000
        try:
            rank = ranks[ranks.index(rank)+1]
        except:
            break
print(value)
print(bigData)

