import numpy as np
import pywt

from Helper import findWatermark, findFiboNr, fillBins

# This whole file was made with the purpose to try out the idea of using SVD with the original algorithm.
# I ended up abandoning this idea because SVD orders the values of variable 's' (line 28), which meant that I couldn't change some of the values and still know to which original position they belonged, because they would rearrange.
# Feel free to explore this idea for future research
def algorithmTimeSeries(d, data, stream, dwtLevel, fibo, nfibo):
    #print(pywt.wavelist())
    x = np.array(data)
    n = len(x)
    # all pairs of indices in x
    # resulting matrix
    result = np.zeros(shape=(n, n))
    # print(x)
    # print(len(a))
    # print(len(b))
    # np.add.at(result, [a, b], (x[a] + x[b]) / 2.0)
    for i in range(n):
        for j in range(n):
            result[i][j] = (x[i]+x[j])/2.0
    coeffs = pywt.wavedec(result, 'db4', 'zero', dwtLevel)
    result_cs = coeffs[0]
    #print(result_cs)
    #res = [int(x) for x in result_cs]

    u,s,v = np.linalg.svd(result_cs)
    print('S')
    print(s)
    bins = fillBins(s, d)

    idIndex = 0
    for kBin in bins:
        iIndex = 0
        for jList in kBin:
            for jValue in jList:
                iIndex += 1
                idIndex += 1
                fiboNr, nNumber = findFiboNr(fibo, nfibo, jValue)
                l = int(np.floor(iIndex / d))
                wl = stream[l]
                if nNumber % 2 == wl:
                    s[idIndex-1] = fiboNr
                elif fiboNr < 0:
                    s[idIndex-1] = nfibo[nNumber + 1]
                else:
                    s[idIndex-1] = fibo[nNumber + 1]
    sigma = np.zeros((u.shape[0], v.shape[0]))
    print("TEST")
    print(s)
    for i in range(min(u.shape[0], v.shape[0])):
        sigma[i, i] = s[i]
    tmp = np.matmul(u, sigma)
    rq = np.matmul(tmp, v)
    coeffs[0] = rq
    print(rq)
    #print(result_cs)
    signal = pywt.waverec(coeffs, 'db4')
    #print(pywt.wavedec(signal, 'db4', 'zero', dwtLevel)[0])
    #signal = signal.astype(np.int16)
    print("Output signal = " + str(signal))
    return signal

def algorithmTimeSeriesReverse(d, data, dwtLevel, fibo, nfibo):
    # x = np.array(data)
    # n = len(x)
    # # all pairs of indices in x
    # # resulting matrix
    # result = np.zeros(shape=(n, n))
    # # print(x)
    # # print(len(a))
    # # print(len(b))
    # # np.add.at(result, [a, b], (x[a] + x[b]) / 2.0)
    # for i in range(n):
    #     for j in range(n):
    #         result[i][j] = (x[i] + x[j]) / 2.0
    print(data)
    coeffs = pywt.wavedec(data, 'db4', 'zero', dwtLevel)
    result_cs = coeffs[0].flatten()

    u,s,v = np.linalg.svd(coeffs[0])
    #print("Result_cs = ")
    print(result_cs)
    print("Length = " + str(len(result_cs)))
    print(s)

    bins = fillBins(s, d)

    watermarkList = []
    #print(bins)
    print("There are " + str(len(bins)) + " bins")
    #s = random.randint(0, min(int(len(result_cs)/d)-1, len(bins)-1))
    #jList = bins[s]
    #print("S = " + str(s))
    #print(jList)
    for jList in bins:
        tmpWList = []
        for kBin in jList:
            zeros = 0
            ones = 0
            for jValue in kBin:
                fiboNr, nNumber = findFiboNr(fibo, nfibo, jValue)
                if nNumber % 2 == 0:
                    zeros += 1
                else:
                    ones += 1
            if zeros > ones:
                tmpWList.append(0)
            elif ones > zeros:
                tmpWList.append(1)
            # elif ones == zeros and ones != 0:
            #     print(jList)
            #     watermark.append(2)
        watermarkList.append(tmpWList)
    watermark = findWatermark(watermarkList)
    return watermarkList