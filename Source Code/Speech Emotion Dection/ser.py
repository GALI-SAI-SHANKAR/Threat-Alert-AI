import pickle
import librosa
import numpy as np
from tensorflow import keras


class ser:
    def mfcc(self):
        file = "./Audios/Dataset/1092_Help_FEA_XX.wav"

        data, sampling_rate = librosa.load(file)
        X = []
        mfcc_feature = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        X.append(mfcc_feature)
        MFCCs = np.array(X)
        return MFCCs

    def ser(self):
        emotions = {
            '0': 'angry',
            '1': 'disgust',
            '2': 'fear',
            '3': 'happy',
            '4': 'neutral',
            '5': 'sad'
        }

        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        MFCCs = self.mfcc()
        p = model.predict(MFCCs, verbose=0)
        yhat_classes = np.argmax(p, 1)
        output = emotions.get(str(yhat_classes[0]))
        if output == 'fear':
            print('Fear')


obj = ser()
obj.ser()
