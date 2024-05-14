import csv
import math
import random
import numpy
import wave

from matplotlib import pyplot as plt
from scipy.io import wavfile

from FiboAudio import algorithmMehdiDavid, algorithmTimeSeries, algorithmTimeSeriesReverse


if __name__ == '__main__':
    d = 5  # random.randint(0, 10)
    s = numpy.random.randint(2, size=(1000,))
    fibo = [0, 0.2, 0.4, 0.6, 0.8, 1]
    for x in range (6, 200):
        #fibo.append(fibo[x-2] + fibo[x-1])
        fibo.append(round(fibo[x-1] * 12)/10)
    print(fibo)
    nfibo = [0, -0.2, -0.4, -0.6, -0.8, -1]
    for x in range(6, 200):
        # fibo.append(fibo[x-2] + fibo[x-1])
        nfibo.append(round(nfibo[x - 1] * 12) / 10)

    # print(fibo)
    # # fl, fh, d = tune(audio)
    # sr, audio = wavfile.read("Test_audio.wav")
    # # audio = a.readframes(-1)

    # print(audio)
    # plt.plot(audio)
    # plt.show()
    # output = algorithmMehdiDavid(d, audio, s, fibo)
    # wavfile.write('output_audio.wav', sr, output)

    with open('WeatherData.txt', 'r') as f:
        first_column = [row[1] for row in csv.reader(f, delimiter=',')]
        tempString = first_column[1:]
    temps = [float(numeric_string) for numeric_string in tempString]

    plt.plot(temps)
    plt.show()

    output = algorithmTimeSeries(d, temps, s, fibo, nfibo)
    plt.plot(output)
    plt.show()
    #output = output[1500:2500]
    with open('WatermarkWeather.txt', 'w') as f:
        for x in output:
            string = str(x)
            f.write(string + '\n')
    watermark = algorithmTimeSeriesReverse(d, output, fibo, nfibo)
    cropStream = s[0:len(watermark)]
    errorRate = 0
    bits = 0
    for x in range(len(cropStream)):
        if cropStream[x] != watermark[x]:
            errorRate += 1
        bits += 1
    print("Error = " + str(errorRate) + " out of a total of " + str(bits) + " used bits in the watermark")
    print(watermark)
    print(cropStream)
