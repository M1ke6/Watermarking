# Watermarking
This project is made as part of the Research Project of the study CSE at the TU Delft in 2024.

It aims to show an adapted algorithm which is originally used to watermark audio signals and translated to be used now with time series data, such as temperature data. 

All tested datasets were found at: https://machinelearningmastery.com/time-series-datasets-for-machine-learning/?__cf_chl_tk=HCfp5sZpQkIi1ogEDfbcfU1QG68kmusGQzl5k.BF4c8-1717766422-0.0.1.1-5034. These datasets can be found in files 'WeatherData.txt' and 'SunspotsData.txt'.
Original audio watermarking algorithm: DOI = 10.1007/s11042-018-5809-8

The algorithm in this repository is written in Python 3.9 and uses packages: numpy==1.24.4, csv, copy, time, matplotlib==3.8.4 (for debugging) and PyWavelets==1.6.0.
The algorithm runs from file 'main.py' and uses files 'Helper.py' and 'TimeSeriesWM.py'. File 'TimeSerSVD.py' was only used to try out the idea of using SVD with the audio watermarking algorithm. I did not turn out to be succesfull in applying that idea, but feel free to use this for future research. File 'FiboAudio.py' was used to create a simple outline of the original audio watermarking algorithm for reference.

The algorithm as it is now shows good robustness against scaling and 1 range cropping attacks (where only 1 range of values is removed). Imperceptibility and robustness against other attacks can be improved. In addition, the way the watermark bit stream is generated can also be made more secure, by e.g. using AES.

