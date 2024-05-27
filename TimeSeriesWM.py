import numpy as np
import pywt

from Helper import findWatermark, findFiboNr, fillBins


def algorithmTimeSeries(d, data, stream, dwtLevel, fibo, nfibo):
    coeffs = pywt.wavedec(data, 'db4', 'zero', dwtLevel)
    result_cs = coeffs[0]

    bins = fillBins(result_cs, d)

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
                    result_cs[idIndex-1] = fiboNr
                elif fiboNr < 0:
                    result_cs[idIndex-1] = nfibo[nNumber + 1]
                else:
                    result_cs[idIndex-1] = fibo[nNumber + 1]
    coeffs[0] = result_cs
    signal = pywt.waverec(coeffs, 'db4')
    return signal

def algorithmTimeSeriesReverse(d, data, dwtLevel, fibo, nfibo):
    coeffs = pywt.wavedec(data, 'db4', 'zero', dwtLevel)
    result_cs = coeffs[0]

    bins = fillBins(result_cs, d)
    watermarkList = []

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









