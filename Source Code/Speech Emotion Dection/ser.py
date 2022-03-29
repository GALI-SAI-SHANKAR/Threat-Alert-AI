import pickle

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

FIG_SIZE = (5, 3)

file = "./Audios/GIRL_Fear/GIRL_help_fear.wav"

signal, sample_rate = librosa.load(file, sr=22050)

hop_length = 512  # in num. of samples
n_fft = 2048  # window in num. of samples

MFCCs = librosa.feature.mfcc(signal, sample_rate, n_fft=n_fft, hop_length=hop_length, n_mfcc=13)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

p = model.predict(MFCCs)

print(p)
