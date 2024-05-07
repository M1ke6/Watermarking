import csv
import math
import random
import numpy
import wave

from matplotlib import pyplot as plt
from scipy.io import wavfile

from FiboAudio import algorithmMehdiDavid, algorithmTimeSeries, algorithmTimeSeriesReverse


if __name__ == '__main__':
    d = 7  # random.randint(0, 10)
    s = numpy.random.randint(2, size=(1000,))
    fibo = [0, 1, 2]
    for x in range (3, 200):
        #fibo.append(fibo[x-2] + fibo[x-1])
        fibo.append(round(fibo[x-1] * 1.3))

    print(fibo)
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
    print(1)
    output = algorithmTimeSeries(d, temps, s, fibo)
    plt.plot(output)
    plt.show()
    with open('WatermarkWeather.txt', 'w') as f:
        for x in output:
            string = str(x)
            f.write(string + '\n')
    watermark = algorithmTimeSeriesReverse(d, output, fibo)
    cropStream = s[0:len(watermark)]
    errorRate = 0
    bits = 0
    for x in range(len(cropStream)):
        if cropStream[x] != watermark[x]:
            errorRate += 1
        bits += 1
    print("Error = " + str(errorRate) + " out of a total of " + str(bits) + " used bits in the watermark")
    print(watermark)
    print(s)
