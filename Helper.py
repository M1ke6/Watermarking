def fillBins(result_cs, d):
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

def findFiboNr(fibo, nfibo, j):
    x = 0
    if j < 0:
        while True:
            if nfibo[x] < j:
                return nfibo[x+1], x+1
            else:
                x += 1
    else:
        while True:
            if fibo[x] > j:
                return fibo[x-1], x-1
            else:
                x += 1

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
