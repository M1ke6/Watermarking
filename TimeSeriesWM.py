import numpy as np
import pywt

from Helper import findFiboNr, fillBins


def algorithmTimeSeries(d, data, stream, dwtLevel, fibo, nfibo):
    out = []
    for i in range(int(np.floor(len(data)/400))):
        temp_data = data[i*d:i*d+400]
        a_2 = [x-1 for x in temp_data]
        a_1 = []
        assert d >= 5
        for z in range(len(a_2)):
            if z == 1:
                a_1.append(complex(1, 1))
            elif z == 3:
                a_1.append(complex(1, -1))
            else:
                a_1.append(complex(1, 0))

        coeffs = pywt.wavedec(a_2, 'db4', 'zero', dwtLevel)
        result_cs = coeffs[0]

        bins = fillBins(result_cs, d)

        idIndex = 0
        for kBin in bins:
            iIndex = 0
            for jList in kBin:
                for jValue in jList:
                    idIndex += 1
                    fiboNr, nNumber = findFiboNr(fibo, nfibo, jValue)
                    l = int(np.floor(iIndex / d))
                    wl = stream[l]
                    iIndex += 1
                    if nNumber % 2 == wl:
                        result_cs[idIndex-1] = fiboNr
                    elif fiboNr < 0:
                        result_cs[idIndex-1] = nfibo[nNumber + 1]
                    else:
                        result_cs[idIndex-1] = fibo[nNumber + 1]
        coeffs[0] = result_cs
        signal = pywt.waverec(coeffs, 'db4')
        concat = []
        for k in range(len(signal)):
            concat.append(signal[k]+a_1[k])
        out += concat
    return out

def algorithmTimeSeriesReverse(d, data, dwtLevel, fibo, nfibo):
    startVal = -1
    for i in range(len(data)):
        if np.imag(data[i]) != 0 and np.imag(data[i+2]) != 0:
            break
        startVal += 1
    temp_data = data[startVal:]
    watermarkList = []
    if len(temp_data) < 400:
        return -1
    for i in range(int(np.floor(len(temp_data) / 400))):
        temp_data = data[i*d+startVal : i * d + 400 + startVal]
        a_2 = [np.real(x)-1 for x in temp_data]

        coeffs = pywt.wavedec(a_2, 'db4', 'zero', dwtLevel)
        result_cs = coeffs[0]

        bins = fillBins(result_cs, d)
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
            watermarkList.append(tmpWList)
    return watermarkList[0]









