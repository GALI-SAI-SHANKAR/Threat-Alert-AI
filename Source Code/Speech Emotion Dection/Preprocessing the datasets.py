import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import librosa
import librosa.display
import os
from IPython.display import Audio, display

GIRL_Fear = "./Audios/Dataset"

data_emotions = {
    'NEU': 'neutral',
    'HAP': 'happy',
    'SAD': 'sad',
    'ANG': 'angry',
    'FEA': 'fear',
    'DIS': 'disgust'}

processed_data = []
data_path = './Audios'

for root, dirs, files in os.walk(data_path):
    for file in files:
        file_path = os.path.join(root, file)

        dataset = root.split('/')[1]
        if dataset == 'Audios\Dataset':
            emotion = data_emotions[file.split('_')[2]]
            processed_data.append([file_path, emotion])

data_df = pd.DataFrame(processed_data, columns=['File_path', 'Emotion'])
# print(data_df)

# data_df.to_csv('data_df.csv')
print(data_df.shape)

plt.title('Count of Emotions', size=16)
sns.countplot(data_df.Emotion)
plt.ylabel('Count', size=12)
plt.xlabel('Emotions', size=12)
sns.despine(top=True, right=True, left=False, bottom=False)
plt.show()


def create_waveplot(data, sr, e):
    plt.figure(figsize=(10, 3))
    plt.title('Waveplot for {} emotion'.format(e), size=15)
    librosa.display.waveplot(data, sr=sr)
    plt.show()


for emotion in data_emotions.values():
    path = (data_df[data_df.Emotion == emotion].iloc[0])[0]
    data, sampling_rate = librosa.load(path)
    create_waveplot(data, sampling_rate, emotion)
    # display(Audio(path))
