import csv
import math
import random
import numpy
import wave

import numpy as np
import pywt
from matplotlib import pyplot as plt
from scipy.io import wavfile

from FiboAudio import algorithmMehdiDavid
from TimeSeriesWM import algorithmTimeSeries, algorithmTimeSeriesReverse

def defineVarsAudio():
    # fl, fh, d = tune(audio)
    sr, audio = wavfile.read("Test_audio.wav")
    # audio = a.readframes(-1)

    print(audio)
    plt.plot(audio)
    plt.show()
    toutput = algorithmMehdiDavid(d, audio, s, fibo, nfibo)
    print("Cropped: " + str(pywt.wavedec(toutput[50:1500], 'Haar', 'zero', 6)[0]))
    # wavfile.write('output_audio.wav', sr, output)
    print(algorithmTimeSeriesReverse(d, toutput, dwtLevel, fibo, nfibo))

def defineVars():
    di = int(input("Enter required framesize:\n"))
    si = numpy.random.randint(2, size=(1000,))
    dwtLeveli = int(input("Enter required dwt level:\n"))
    multRate = int(input("Enter multiplication rate of reference sequence:\n"))
    filename = input("Enter path to input file:\n")
    with open(filename, 'r') as g:
        first_column = [row[1] for row in csv.reader(g, delimiter=',')]
        tempString = first_column[1:]
    tempsi = [float(numeric_string) for numeric_string in tempString]
    fiboi = [0, 1, 2]
    for k in range(3, 100):
        tmp = round(fiboi[k-1]*multRate/10)
        if tmp == fiboi[k-1]:
            tmp += 1
        fiboi.append(tmp)
    nfiboi = [0, -1, -2]
    for k in range(3, 100):
        tmp = round(nfiboi[k - 1] * multRate/10)
        if tmp == nfiboi[k - 1]:
            tmp -= 1
        nfiboi.append(tmp)

    plt.plot(tempsi)
    plt.title("Original data")
    plt.show()

    return di, si, dwtLeveli, tempsi, fiboi, nfiboi

if __name__ == '__main__':
    # coeffs = pywt.wavedec(temps, 'db4', 'zero', dwtLevel)[0]
    # minVal = min(coeffs)
    # maxVal = max(coeffs)
    # startVal = 0
    # if minVal > 5:
    #     startVal = int(minVal)
    #
    # multRate = 16
    # if int(maxVal)-int(minVal) > 50:
    #     multRate = 14
    # if int(maxVal) - int(minVal) > 130:
    #     multRate = 15
    # if int(maxVal)-int(minVal) > 1:
    #     multRate = 16

    d, s, dwtLevel, temps, fibo, nfibo = defineVars()
    output = algorithmTimeSeries(d, temps, s, dwtLevel, fibo, nfibo)
    print("AVG = " + str(np.average(output)))
    print(output.shape)
    # graph = np.zeros(output.shape[0])
    # for i in range(len(output[0])):
    #     graph[i] = output[i][i]
    plt.plot(output)
    plt.title("Watermarked data")
    plt.show()
    output = [x * 1.2 for x in output]
    #output = np.concatenate([output[0:500], output[700:1000]])
    #graph = graph[50:1500]
    with open('WatermarkWeather.txt', 'w') as f:
        for x in output:
            string = str(x)
            f.write(string + '\n')
    watermark = algorithmTimeSeriesReverse(d, output, dwtLevel, fibo, nfibo)
    cropStream = s[0:len(watermark[0])]
    errorRate = 0
    bits = 0
    for x in range(len(cropStream)):
        if cropStream[x] != watermark[0][x]:
            errorRate += 1
        bits += 1
    print("Error = " + str(errorRate) + " out of a total of " + str(bits) + " used bits in the watermark")
    print(watermark)
    print(s)
