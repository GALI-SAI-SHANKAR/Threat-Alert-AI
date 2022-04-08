import librosa
import numpy
import numpy as np
import pandas as pd
import librosa.display
import seaborn as sns
import matplotlib.pyplot as plt


def noise(data, random=False, rate=0.035, threshold=0.075):
    if random:
        rate = np.random.random() * threshold
    noise_amp = rate * np.random.uniform() * np.amax(data)
    data = data + noise_amp * np.random.normal(size=data.shape[0])
    return data


def stretch(data, rate=0.8):
    return librosa.effects.time_stretch(data, rate)


def shift(data, rate=1000):
    shift_range = int(np.random.uniform(low=-5, high=5) * rate)
    return np.roll(data, shift_range)


def pitch(data, sampling_rate, pitch_factor=0.7, random=False):
    if random:
        pitch_factor = np.random.random() * pitch_factor
    return librosa.effects.pitch_shift(data, sampling_rate, pitch_factor)


data_df = pd.read_csv('data_df.csv')
emotion = 'fear'
path = (data_df[data_df.Emotion == emotion].iloc[0])[1]
data, sampling_rate = librosa.load(path)
data_copy = data


# plt.figure(figsize=(14, 4))
# librosa.display.waveplot(data, sampling_rate)
# plt.show()
#
# noised_data = noise(data, random=True)
# plt.figure(figsize=(14, 4))
# librosa.display.waveplot(y=noised_data, sr=sampling_rate)
# plt.show()
#
# stretched_data = stretch(data, rate=0.5)
# plt.figure(figsize=(14, 4))
# librosa.display.waveplot(y=stretched_data, sr=sampling_rate)
# plt.show()
#
# shifted_data = shift(data)
# plt.figure(figsize=(14, 4))
# librosa.display.waveplot(y=shifted_data, sr=sampling_rate)
# plt.show()
#
# pitched_data = pitch(data, sampling_rate, pitch_factor=0.5, random=True)
# plt.figure(figsize=(14, 4))
# librosa.display.waveplot(y=pitched_data, sr=sampling_rate)
# plt.show()

def mfcc(data, sampling_rate):
    mfcc_feature = librosa.feature.mfcc(y=data, sr=sampling_rate )
    return np.ravel(mfcc_feature.T)


path = np.array(data_df["File_path"])[100]
data, sampling_rate = librosa.load(path, duration=2.5, offset=0.6)
print("Length of data: ", len(data))
print("MFrequency Cepstral Coefficients: ", mfcc(data, sampling_rate).shape)


def get_features(path, duration=2.5, offset=0.6):
    data, sampling_rate = librosa.load(path, duration=duration, offset=offset)
    return mfcc(data, sampling_rate)


data, sampling_rate = librosa.load(path)
type(np.ravel(librosa.feature.mfcc(y=data, sr=sampling_rate).T))
numpy.ndarray
X, Y = [], []
print('Feature processing...')
for path, emotion, index in zip(data_df.File_path, data_df.Emotion, range(data_df.File_path.shape[0])):
    data, sampling_rate = librosa.load(path, duration=2.5, offset=0.6)
    mfcc_feature = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
    if index % 1000 == 0:
        print(f"{index} samples has been processed...")
    X.append(mfcc_feature)
    Y.append(emotion)
print('Done.')

features_path = './features_rmse_mfcc.csv'

extracted_df = pd.DataFrame(X)
extracted_df['labels'] = Y
extracted_df.to_csv(features_path, index=False)
print(extracted_df.head(100))
print(extracted_df.shape)
