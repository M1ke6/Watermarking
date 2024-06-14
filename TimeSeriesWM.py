import numpy as np
import pywt

from Helper import findFiboNr, fillBins


def algorithmTimeSeries(fbin, d, w, dwt, fibo, nfibo, fbarker=400):    # Watermarking embedding algorithm
                                                                            # Fbarker is used to create sections to embed a barker code (in the form of imaginary values) in each of them to improve robustness). Value can be edited based on size of input data
    out = []
    for i in range(int(np.floor(len(d)/fbarker))):                          # Split data in sections with size fbarker
        temp_data = d[i*fbin:i*fbin+fbarker]
        a_2 = [x-1 for x in temp_data]                                      # Split a such that a_1+a_2=a
        a_1 = []
        assert fbin >= 5
        for z in range(len(a_2)):                                           # Embed barker code in a_1 at position 1 and 3 of the section
            if z == 1:
                a_1.append(complex(1, 1))
            elif z == 3:
                a_1.append(complex(1, -1))
            else:
                a_1.append(complex(1, 0))

        coeffs = pywt.wavedec(a_2, 'db4', 'zero', dwt)          # Run the DWT on a_2 with DWT level equal the variable value 'dwt'
        result_cs = coeffs[0]

        bins = fillBins(result_cs, fbin)                                    # Divide the coefficients into bins with size fbin

        idIndex = 0
        for kBin in bins:
            iIndex = 0
            for jList in kBin:
                for jValue in jList:
                    idIndex += 1
                    fiboNr, nNumber = findFiboNr(fibo, nfibo, jValue)       # Find the value in fibo and nfibo that is closest to the magnitude of the coefficient
                    l = int(np.floor(iIndex / fbin))                        # Each frame has an assigned bit (e.g. the first fbin coefficients get the same watermark bit through this formula)
                    wl = w[l]
                    iIndex += 1
                    if nNumber % 2 == wl:                                   # If the position of the found value in fibo/nfibo is even and the bit is 0, or odd and 1 respectively. The magnitude is changed to the value found in fibo/nfibo
                        result_cs[idIndex-1] = fiboNr
                    elif fiboNr < 0:                                        # Else the magnitude changes to one value higher in the nfibo sequence if negative
                        result_cs[idIndex-1] = nfibo[nNumber + 1]
                    else:                                                   # And one higher in the fibo sequence if the coefficient was positive
                        result_cs[idIndex-1] = fibo[nNumber + 1]
        coeffs[0] = result_cs
        signal = pywt.waverec(coeffs, 'db4')                        # Apply IDWT
        concat = []
        for k in range(len(signal)):                                        # Merge a_1 and a_2 back together
            concat.append(signal[k]+a_1[k])
        out += concat
    return out

def algorithmTimeSeriesReverse(fbin, d, dwt, fibo, nfibo, fbarker=400):
    startVal = -1
    for i in range(len(d)):
        if np.imag(d[i]) != 0 and np.imag(d[i+2]) != 0:                     # Find the starting point of the section by detecting the barker code
            break
        startVal += 1
    temp_data = d[startVal:]
    watermarkList = []
    if len(temp_data) < fbarker:                                            # If nothing is found and the resulting section is smaller than the size of fbarker we try to detect one of the two values of the barker code (so either at position 1 or 3 in the section)
        startVal = -1
        for i in range(len(d)):
            if np.imag(d[i]) != 0:
                if np.imag(d[i]) == -1:
                    startVal -= 2
            startVal += 1
        temp_data = d[startVal:]
        if len(temp_data) < fbarker:                                        # If all positions containing the barker code are modified and we don't find anything, we use the starting point of the watermarked data as reference
            temp_data = d
    for i in range(int(np.floor(len(temp_data) / fbarker))):                # We split the data into sections with size fbarker
        tmp_data = temp_data[i*fbin : i * fbin + fbarker]
        if len(tmp_data) < fbarker:                                         # If the length of the section is less than fbarker we don't consider this section as the watermark embedded will not be complete
            continue
        a_2 = [np.real(x)-1 for x in tmp_data]                              # Split data such that a_1+a_2=data, a_1 isn't needed anymore in extracting phase

        coeffs = pywt.wavedec(a_2, 'db4', 'zero', dwt)          # Apply DWT with the DWT level being equal to the variable value of 'dwt'
        result_cs = coeffs[0]

        bins = fillBins(result_cs, fbin)                                    # Divide the DWT coefficients into bins with size fbin
        for jList in bins:
            tmpWList = []
            for kBin in jList:
                zeros = 0
                ones = 0
                for jValue in kBin:
                    fiboNr, nNumber = findFiboNr(fibo, nfibo, jValue)       # Find the value in fibo/nfibo that is closest to the magnitude of the coefficient
                    if nNumber % 2 == 0:                                    # If the position of the found value is even, increase the value of 'zeros'
                        zeros += 1
                    else:                                                   # If the position of the found value is odd, increase the value of 'zeros'
                        ones += 1
                if zeros > ones:                                            # If more values were positioned at even indexes, the watermark bit was a 0
                    tmpWList.append(0)
                elif ones > zeros:                                          # If more values were positioned at odd indexes, the watermark bit was a 1
                    tmpWList.append(1)                                      # NOTE: therefore always use an odd value for variable fbin, to avoid ambiguity
            watermarkList.append(tmpWList)
    return watermarkList[0]                                                 # The algorithm works in a way that the first found watermark is the (most) correct one, no matter at which section you start.
                                                                            # So the for loop at line 70 is mostly for debugging purposes. When algorithm is used with larger datasets and the run time becomes an issue, lines 70 to 96 could be rewritten









