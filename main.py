import copy
import csv
import random
import time

import numpy
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
    si = numpy.random.randint(2, size=(50,))
    dwtLeveli = int(input("Enter required dwt level:\n"))
    multRate = int(input("Enter multiplication rate of reference sequence (multiply the preferred rate by 10, so for 1.2 enter 12):\n"))
    filename = 'SunspotsData.txt'
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

def testImper():
    print("AVG original data = " + str(np.average(temps)))
    print("Min original data = " + str(np.min(temps)))
    print("Max original data = " + str(np.max(temps)))
    now = time.time()
    cur = 0
    outputmp = []
    for i in range(100):
        outputmp = algorithmTimeSeries(d, temps, s, dwtLevel, fibo, nfibo)
        for j in range(len(outputmp)):
            cur += np.real(outputmp[j])-temps[j]
    print("Time spent on 100 times embedding: " + str(time.time()-now))
    print("AVG watermarked data = " + str(np.average(outputmp)))
    print("Min watermarked data = " + str(np.min(outputmp)))
    print("Max watermarked data = " + str(np.max(outputmp)))
    print("Avg value change in data = " + str(cur))
    return outputmp

def calcError(watermark, cropStream):
    errorRate = 0
    bits = 0
    for x in range(len(cropStream)):
        if cropStream[x] != watermark[x]:
            errorRate += 1
        bits += 1
    print("Error = " + str(errorRate) + " out of a total of " + str(bits) + " used bits in the watermark")
    return errorRate/bits

def testRobust(watermarked, attackNr):
    averageErrorRate = 0
    count = 0
    totalCount = 0
    listS = []
    listX = []
    percentData = 100/int(input("How much percentage of the data do you want to be affected by the attack? Only enter an integer value.\nPS: value doesn't matter for scaling attacks.\n"))
    if attackNr == 1:
        for i in range(100):
            copyOutput = copy.deepcopy(watermarked)
            ints = random.sample(range(1, len(watermarked)), int(len(watermarked) / percentData))
            for sample in ints:
                copyOutput[sample] = 0          # For zero-out and deletion attacks
            j = len(copyOutput) - 1
            while j > 0:
                if copyOutput[j] == 0:
                    del copyOutput[j]
                j -= 1
            watermark = algorithmTimeSeriesReverse(d, copyOutput, dwtLevel, fibo, nfibo)
            if watermark == -1:
                continue
            else:
                count += 1
            averageErrorRate += calcError(watermark, s[0:len(watermark)])
            totalCount += 1
    if attackNr == 2:
        for i in range(100):
            copyOutput = copy.deepcopy(watermarked)
            ints = random.sample(range(1, len(watermarked)), int(len(watermarked) / percentData))
            for sample in ints:
                copyOutput[sample] = random.random()*np.max(watermarked)         # For editing attacks
            watermark = algorithmTimeSeriesReverse(d, copyOutput, dwtLevel, fibo, nfibo)
            if watermark == -1:
                continue
            else:
                count += 1
            averageErrorRate += calcError(watermark, s[0:len(watermark)])
            totalCount += 1
    if attackNr == 3:
        for i in range(100):
            copyOutput = copy.deepcopy(watermarked)
            ints = random.sample(range(1, len(watermarked)), int(len(watermarked) / percentData))
            for sample in ints:
                copyOutput.insert(sample, random.random()*np.max(watermarked))   # For insertion attacks
            watermark = algorithmTimeSeriesReverse(d, copyOutput, dwtLevel, fibo, nfibo)
            if watermark == -1:
                continue
            else:
                count += 1
            averageErrorRate += calcError(watermark, s[0:len(watermark)])
            totalCount += 1
    if attackNr == 4:
        for i in range(100):
            copyOutput = copy.deepcopy(watermarked)
            ints = random.sample(range(1, len(watermarked)), int(len(watermarked) / percentData))
            for sample in ints:
                copyOutput[sample] = 0                                      # For zero-out and deletion attacks
            watermark = algorithmTimeSeriesReverse(d, copyOutput, dwtLevel, fibo, nfibo)
            if watermark == -1:
                continue
            else:
                count += 1
            averageErrorRate += calcError(watermark, s[0:len(watermark)])
            totalCount += 1
    if attackNr == 5:
        scalingRate = 0.2
        while scalingRate < 5:
            copyOutput = copy.deepcopy(watermarked)
            copyOutput = [y * scalingRate for y in copyOutput]  # For scaling attacks
            watermark = algorithmTimeSeriesReverse(d, copyOutput, dwtLevel, fibo, nfibo)
            if watermark == -1:
                continue
            else:
                count += 1
            error = calcError(watermark, s[0:len(watermark)])
            averageErrorRate += error
            totalCount += 1
            listS.append(error)
            listX.append(scalingRate)
        plt.plot(listX, listS)
        plt.show()


    print("We got output for " + str(count) + " out of " + str(totalCount) + " cases.")
    print("The average errorrate was: " + str(averageErrorRate/count))
    with open('WatermarkWeather.txt', 'w') as f:    # Debugging purposes
        for z in watermarked:
            string = str(z)
            f.write(string + '\n')

if __name__ == '__main__':
    d, s, dwtLevel, temps, fibo, nfibo = defineVars()

    if int(input("Do you want to test for imperceptibility? 0: No, 1: Yes\n")) == 1:
        output = testImper()
    else:
        output = algorithmTimeSeries(d, temps, s, dwtLevel, fibo, nfibo)

    plt.plot(np.real(output))
    plt.title("Watermarked data")
    plt.show()

    testR = input("Which attacks do you want to test for? 0: None, 1: Deletion, 2: Editing, 3: Insertion, 4: Zero-out, 5: Scaling\n")
    if 0 < int(testR) < 6:
        testRobust(output, int(testR))

    watermarkOutput = algorithmTimeSeriesReverse(d, output, dwtLevel, fibo, nfibo)
    print("-------------------------------------")
    print("Output for input values with entire original dataset: ")
    print("Extracted watermark: " + str(watermarkOutput))
    listRef = []
    for element in s[0:len(watermarkOutput)]:
        listRef.append(element)
    print("Reference watermark: " + str(listRef))

