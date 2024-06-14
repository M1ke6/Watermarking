import copy
import csv
import random
import time

import numpy
import numpy as np
from matplotlib import pyplot as plt

from TimeSeriesWM import algorithmTimeSeries, algorithmTimeSeriesReverse


def defineVars():
    fbin1 = int(input("Enter required framesize:\n"))                       # Stores frame size (how long watermark should be. Note: if the value is too high and the dwt is too high, the watermark will be shorter)
    w1 = numpy.random.randint(2, size=(50,))                                # Randomly generated watermark bit stream, can be changed to a different way of generating
    dwtLevel1 = int(input("Enter required dwt level:\n"))                   # Stores the dwt level that should be applied to the data
    mult1 = int(input("Enter multiplication rate of reference sequence "
                      "(multiply the preferred rate by 10, so for 1.2 enter 12):\n"))    # Stores the multiplication rate (x10) that should be between the values of the reference set
    filename = 'SunspotsData.txt'                                           # File name containing input data
    with open(filename, 'r') as g:                                          # Input data should start from the second row and be in the second column
        first_column = [row[1] for row in csv.reader(g, delimiter=',')]
        tempString = first_column[1:]
    d1 = [float(numeric_string) for numeric_string in tempString]           # Stores input data (only float time series data has been tested with)
    fibo1 = [0, 1, 2]                                                       # Stores reference set for positive data
    for k in range(3, 100):
        tmp = round(fibo1[k-1]*mult1/10)
        if tmp == fibo1[k-1]:
            tmp += 1
        fibo1.append(tmp)
    nfibo1 = [0, -1, -2]                                                    # Stores reference set for negative data
    for k in range(3, 100):
        tmp = round(nfibo1[k - 1] * mult1/10)
        if tmp == nfibo1[k - 1]:
            tmp -= 1
        nfibo1.append(tmp)

    #Debug purposes
    plt.plot(d1)
    plt.title("Original data")
    plt.show()

    return fbin1, w1, dwtLevel1, d1, fibo1, nfibo1

def testImper():                                            # Test imperceptibility algorithm by calculating the average, minimal and maximal value of the original vs watermarked data.
                                                            # Also the average change in individual value is calculated
    print("AVG original data = " + str(np.average(d)))
    print("Min original data = " + str(np.min(d)))
    print("Max original data = " + str(np.max(d)))
    now = time.time()
    cur = 0
    avg = 0
    minT = 0
    maxT = 0
    outputmp = []
    for i in range(100):
        tmpW = numpy.random.randint(2, size=(50,))
        outputmp = algorithmTimeSeries(fbin, d, tmpW, dwt, fibo, nfibo)
        avg += np.average(outputmp)
        minT += np.min(outputmp)
        maxT += np.max(outputmp)
        for j in range(len(outputmp)):
            cur += np.abs(np.real(outputmp[j])-d[j])
    print("Time spent on 100 times embedding: " + str(time.time()-now))
    print("AVG watermarked data = " + str(avg/100))
    print("Min watermarked data = " + str(minT/100))
    print("Max watermarked data = " + str(maxT/100))
    print("Avg value change in data = " + str(cur/100/len(outputmp)))

    plt.plot(np.real(outputmp))
    plt.title("Watermarked data")
    plt.show()

    return outputmp

def calcError(watermark, cropStream):           # Compares generated bit stream with extracted watermark to calculate how many bits don't match
    errorRate = 0
    bits = 0
    for x in range(len(cropStream)):
        if cropStream[x] != watermark[x]:
            errorRate += 1
        bits += 1
    print("Error = " + str(errorRate) + " out of a total of " + str(bits) + " used bits in the watermark")
    return errorRate/bits

def testRobust(watermarked, attackNr):          # Tests robustness by running the chosen attack 100 times and seeing how well the watermark can be extracted
    averageErrorRate = 0
    count = 0
    totalCount = 0
    listS = []
    listX = []
    percentData = 100/int(input("How much percentage of the data do you want to be affected by the attack? Only enter an integer value.\nPS: value doesn't matter for scaling attacks.\n"))
    if attackNr == 1:           # For deletion attacks
        for i in range(100):
            copyOutput = copy.deepcopy(watermarked)
            ints = random.sample(range(1, len(watermarked)), int(len(watermarked) / percentData))   # Random samples generated with the chosen amount
            for sample in ints:
                copyOutput[sample] = 0      # First each deleted index will be set to 0, after which it will be removed, so that we don't have to worry about the shrinking size of the dataset (which will manipulate the sampled indexes)
            j = len(copyOutput) - 1
            while j > 0:
                if copyOutput[j] == 0:
                    del copyOutput[j]
                j -= 1
            watermark = algorithmTimeSeriesReverse(fbin, copyOutput, dwt, fibo, nfibo)
            if watermark == -1: # Check if watermark exists
                continue
            else:
                count += 1
            averageErrorRate += calcError(watermark, w[0:len(watermark)])
            totalCount += 1
    if attackNr == 2:           # For editing attacks
        for i in range(100):
            copyOutput = copy.deepcopy(watermarked)
            ints = random.sample(range(1, len(watermarked)), int(len(watermarked) / percentData))   # Random samples generated with the chosen amount
            for sample in ints:
                copyOutput[sample] = copyOutput[sample]-np.max(watermarked)/10+random.random()*np.max(watermarked)/5     # For each sample, the value is edited by at most 10% positive or negative of the original value
            watermark = algorithmTimeSeriesReverse(fbin, copyOutput, dwt, fibo, nfibo)
            if watermark == -1: # Check if watermark exists
                continue
            else:
                count += 1
            averageErrorRate += calcError(watermark, w[0:len(watermark)])
            totalCount += 1
    if attackNr == 3:           # For insertion attacks
        for i in range(100):
            copyOutput = copy.deepcopy(watermarked)
            ints = random.sample(range(1, len(watermarked)), int(len(watermarked) / percentData))   # Random samples generated with the chosen amount
            for sample in ints:
                copyOutput.insert(sample, copyOutput[sample-1]-np.max(watermarked)/10+random.random()*np.max(watermarked)/5)    # For each sample, the value is inserted by at most 10% positive or negative of the value to its left
            watermark = algorithmTimeSeriesReverse(fbin, copyOutput, dwt, fibo, nfibo)
            if watermark == -1: # Check if watermark exists
                continue
            else:
                count += 1
            averageErrorRate += calcError(watermark, w[0:len(watermark)])
            totalCount += 1
    if attackNr == 4:           # For zero-out attacks
        for i in range(100):
            copyOutput = copy.deepcopy(watermarked)
            ints = random.sample(range(1, len(watermarked)), int(len(watermarked) / percentData))   # Random samples generated with the chosen amount
            for sample in ints:
                copyOutput[sample] = 0
            watermark = algorithmTimeSeriesReverse(fbin, copyOutput, dwt, fibo, nfibo)
            if watermark == -1: # Check if watermark exists
                continue
            else:
                count += 1
            averageErrorRate += calcError(watermark, w[0:len(watermark)])
            totalCount += 1
    if attackNr == 5:           # For scaling attacks
        scalingRate = 0.7       # Value of scalingRate and stopping condition of while loop can be set to test more values
        while scalingRate < 2:
            copyOutput = copy.deepcopy(watermarked)
            copyOutput = [y * scalingRate for y in copyOutput]
            watermark = algorithmTimeSeriesReverse(fbin, copyOutput, dwt, fibo, nfibo)
            if watermark == -1: # Check if watermark exists
                continue
            else:
                count += 1
            error = calcError(watermark, w[0:len(watermark)])
            averageErrorRate += error
            totalCount += 1
            listS.append(error)         # For output graph: y-axis
            listX.append(scalingRate)   # For output graph: x-axis
            scalingRate += 0.1          # Measured with steps of 0.1, can be edited to suit different test
            scalingRate = np.round(scalingRate, 1)
        plt.plot(listX, listS)
        plt.show()


    print("We got output for " + str(count) + " out of " + str(totalCount) + " cases.")
    print("The average errorrate was: " + str(averageErrorRate/count))

if __name__ == '__main__':
    fbin, w, dwt, d, fibo, nfibo = defineVars()         # Define input variables for the algorithm

    if int(input("Do you want to test for imperceptibility? 0: No, 1: Yes\n")) == 1:
        output = testImper()                                            # Run tests for imperceptibility and return the watermarked data
    else:
        output = algorithmTimeSeries(fbin, d, w, dwt, fibo, nfibo)      # Run the watermarking embedding algorithm

    testR = input("Which attacks do you want to test for? 0: None, 1: Deletion, 2: Editing, 3: Insertion, 4: Zero-out, 5: Scaling\n")
    if 0 < int(testR) < 6:
        testRobust(output, int(testR))                                  # Run tests for robustness with the chosen attack

    watermarkOutput = algorithmTimeSeriesReverse(fbin, output, dwt, fibo, nfibo)    # Run the watermarking extraction algorithm
    print("-------------------------------------")                      # Show the output
    print("Output for input values with entire original dataset: ")
    print("Extracted watermark: " + str(watermarkOutput))
    listRef = []
    for element in w[0:len(watermarkOutput)]:
        listRef.append(element)
    print("Reference watermark: " + str(listRef))

