import numpy as np
import pywt
from matplotlib import pyplot as plt
def algorithmMehdiDavid(d, audio, stream, fibo):
    coeffs = pywt.wavedec(audio, 'Haar', 'zero', 6)
    result_cs = coeffs[0]
    print(result_cs)

    b = np.linspace(0, 70, 11)
    count = 0
    indexes = np.digitize(result_cs, b)

    bins = [[] for _ in range(100)]
    for r in result_cs:
        bins[indexes[count]].append((r, count))
        count += 1
    iIndex = 0
    for kBin in bins:
        for (jValue, cCount) in kBin:
            iIndex += 1
            jValue = np.abs(jValue)
            fiboNr, nNumber = findFiboNr(fibo, jValue)
            l = int(np.floor(iIndex/d))
            wl = stream[l]
            if nNumber % 2 == wl:
                result_cs[cCount] = fiboNr
            else:
                result_cs[cCount] = fibo[nNumber+1]
    coeffs[0] = result_cs
    print(result_cs)
    signal = pywt.waverec(coeffs, 'Haar')

    plt.plot(signal)
    plt.show()
    signal = signal.astype(np.int16)
    print(signal)
    return signal

def algorithmTimeSeries(d, data, stream, fibo):
    coeffs = pywt.wavedec(data, 'Haar', 'zero', 6)
    result_cs = coeffs[0]
    print(result_cs)

    # maxBin = 70
    # b = np.linspace(0, maxBin, int(maxBin/d+1))
    # count = 0
    # indexes = np.digitize(result_cs, b)

    # bins = [[] for _ in range(100)]
    # for r in result_cs:
    #     bins[indexes[count]].append((abs(r), count))
    #     count += 1
    bins = [[] for _ in range(int(len(result_cs)/6))]
    e = 0
    f = 0
    for index in range(0, len(result_cs)):
        print(e)
        print(f)
        bins[f].append(result_cs[index])
        if e < 7:
            e += 1
        else:
            e = 0
            f += 1

    iIndex = 0
    for kBin in bins:
        for jValue in kBin:
            iIndex += 1
            jValue = np.abs(jValue)
            fiboNr, nNumber = findFiboNr(fibo, jValue)
            l = int(np.floor(iIndex / d))
            wl = stream[l]
            if nNumber % 2 == wl:
                result_cs[iIndex-1] = fiboNr
            else:
                result_cs[iIndex-1] = fibo[nNumber + 1]
    coeffs[0] = result_cs
    print(result_cs)
    signal = pywt.waverec(coeffs, 'Haar')

    signal = signal.astype(np.int16)
    print(signal)
    return signal

def algorithmTimeSeriesReverse(d, data, fibo):
    coeffs = pywt.wavedec(data, 'Haar', 'zero', 6)
    result_cs = coeffs[0]
    print(result_cs)
    print("Length = " + str(len(result_cs)))

    # maxBin = int(np.ceil(max(result_cs)))
    # b = np.linspace(0, maxBin, int(maxBin / d + 1))
    # count = 0
    # indexes = np.digitize(result_cs, b)
    #
    # bins = [[] for _ in range(maxBin+1)]
    # for r in result_cs:
    #     print(indexes[count])
    #     bins[indexes[count]].append((r, count))
    #     count += 1

    bins = [[] for _ in range(int(len(result_cs)))]
    e = 0
    f = 0
    for index in range(0, len(result_cs)):
        bins[f].append(result_cs[index])
        if e < d-1:
            e += 1
        else:
            e = 0
            f += 1
    iIndex = 0
    watermark = []
    print(bins)
    print("There are " + str(len(bins)) + " bins")
    for kBin in bins:
        zeros = 0
        ones = 0
        for jValue in kBin:
            iIndex += 1
            jValue = np.abs(jValue)
            fiboNr, nNumber = findFiboNr(fibo, jValue)
            if nNumber % 2 == 0:
                zeros += 1
            else:
                ones += 1
        if zeros > ones:
            watermark.append(0)
        elif ones > zeros:
            watermark.append(1)
        # else:
        #     print(9999)
    return watermark

def findFiboNr(fibo, j):
    x = 0
    while True:
        if fibo[x] > j:
            disA = np.abs(fibo[x]-j)
            disB = np.abs(fibo[x-1]-j)
            if disA < disB:
                return fibo[x], x
            else:
                return fibo[x-1], x - 1
        else:
            x += 1




# def analyseAudio(audio):
#     cap =
#     return 1,2,3
# def tune():
#     CAP_req = 10
#     ODG_req = -0.5
#     BER_req = 5
#     fl = 12000
#     fh = 16000
#     d = 5
#
#     while True:
#         cap, odg, ber = analyseAudio(audio)
#         if cap > CAP_req:
#             if odg > ODG_req:
#                 if ber > BER_req:
#                     return fl, fh, d
#                 else:
#                     fh -= 100
#             else:
#                 fl += 100
#         else:
#             d -= 1




