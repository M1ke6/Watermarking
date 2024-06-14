def fillBins(result_cs, d):     # Create a list and fill the coefficients into bins with size n*d*d, where n is any positive value
                                # This means we have d values per watermark bit and d watermark bits in the watermark
    bins = [[[] for _ in range(d+1)] for _ in range(int(len(result_cs)/d/d)+1)]
    e = 0
    f = 0
    g = 0
    for index in range(0, len(result_cs)):
        bins[g][f].append(result_cs[index])
        if e < d - 1:
            e += 1
        else:
            e = 0
            if f < d - 1:
                f += 1
            else:
                f = 0
                g += 1
    return bins

def findFiboNr(fibo, nfibo, j):     # Find the number in fibo/nfibo that is closest to the value of j
    x = 0
    if j < 0:
        while True:
            if nfibo[x] < j:
                return nfibo[x], x
            else:
                x += 1
    else:
        while True:
            if fibo[x] > j:
                return fibo[x-1], x-1
            else:
                x += 1

#Debugging purposes, not used in algorithm
def findWatermark(wList):
    watermark = []
    for x in range(len(wList[0])):
        zeros = 0
        ones = 0
        for l in wList:
            if len(l) == len(wList[0]):
                if l[x] == 0:
                    zeros += 1
                else:
                    ones += 1
        if zeros > ones:
            watermark.append(0)
        else:
            watermark.append(1)
    return watermark
