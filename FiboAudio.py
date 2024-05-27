import numpy as np
import pywt
from matplotlib import pyplot as plt
def algorithmMehdiDavid(d, audio, stream, fibo, nfibo):
    #fl, fh, d = tune(audio, d)
    coeffs = pywt.wavedec(audio, 'Haar', 'zero', 6)
    result_cs = coeffs[0]
    #print(result_cs)

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
            fiboNr, nNumber = findFiboNr(fibo, nfibo, jValue)
            l = int(np.floor(iIndex/d))
            wl = stream[l]
            if nNumber % 2 == wl:
                result_cs[cCount] = fiboNr
            else:
                result_cs[cCount] = fibo[nNumber+1]
    coeffs[0] = result_cs
    print("Test")
    print(result_cs)
    signal = pywt.waverec(coeffs, 'Haar')

    plt.plot(signal)
    plt.show()
    signal = signal.astype(np.int16)
    print(signal)
    return signal

def findFiboNr(fibo, nfibo, j):
    x = 0
    if j < 0:
        while True:
            if nfibo[x] <= j:
                disA = np.abs(nfibo[x] - j)
                disB = np.abs(nfibo[x - 1] - j)
                if disA < disB:
                    return nfibo[x], x
                else:
                    return nfibo[x - 1], x - 1
            else:
                x += 1
    else:
        while True:
            if fibo[x] >= j:
                disA = np.abs(fibo[x] - j)
                disB = np.abs(fibo[x + 1] - j)
                if disA < disB:
                    return fibo[x], x
                else:
                    return fibo[x + 1], x + 1
            else:
                x += 1

def analyseAudio(audio):
    return 1
def tune(audio, d):
    CAP_req = 10
    ODG_req = -0.5
    BER_req = 5
    fl = 12000
    fh = 16000

    while True:
        cap, odg, ber = analyseAudio(audio)
        if cap > CAP_req:
            if odg > ODG_req:
                if ber > BER_req:
                    return fl, fh, d
                else:
                    fh -= 100
            else:
                fl += 100
        else:
            d -= 1




