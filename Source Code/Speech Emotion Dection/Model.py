import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import pandas as pd
from tensorflow.keras.utils import to_categorical

extracted_df = pd.read_csv('features_rmse_mfcc.csv')

le = preprocessing.LabelEncoder()
le.fit(extracted_df.labels)
extracted_df['categorical_label'] = le.transform(extracted_df.labels)
Y = extracted_df.categorical_label

Y = to_categorical(Y)

X = np.array(X)
Y = np.array(Y)
X = np.squeeze(X)
X = np.expand_dims(X,-1)
x_train, x_test, y_train, y_test = train_test_split(X, Y,test_size=0.3, random_state=42)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train,test_size=0.05, random_state=42)