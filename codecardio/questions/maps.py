def mostFrequent(a):
    maxValue = None
    maxCount = 0
    counts = dict()
    for element in a:
        count = counts[element] if (element in counts) else 0
        count += 1
        counts[element] = count
        if (count > maxCount):
            maxCount = count
            maxValue = element
    return maxValue

print mostFrequent([2,5,3,4,6,4,2,4,5])