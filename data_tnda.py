import numpy as np
from sklearn.model_selection import train_test_split
from torch_geometric.data import Data, InMemoryDataset
import torch
from torch_geometric.data import DataLoader
import os
import pandas as pd
import pickle as cp
from gtda.time_series import SlidingWindow
from sklearn.preprocessing import MinMaxScaler


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def load_data(path):
    # df = pd.read_csv('mhealth_raw_data.csv')
    df = pd.read_csv('pamap2_raw_data.csv')
    df = pd.read_csv(path)
    x_columns = list(df.columns)
    x_columns.remove("Activity")
    x = df[x_columns][df["Activity"] != 0]
    y = df["Activity"][df["Activity"] != 0]
    return x, y


def data_preprocesssing(data, label, size, stride):
    Scaler = MinMaxScaler()
    data_ = Scaler.fit_transform(data)
    SW = SlidingWindow(size=size, stride=stride)
    X, y = SW.fit_transform_resample(data_, label)
    return X, y


# You can type the path of your dataset
path = 'MHEALTHDATASET/'
data, label = load_data(path)
print(data.shape)
corrcoef = np.corrcoef(data.T)
np.savetxt('data_/adj_pamap2.csv', corrcoef, delimiter=',')

data_processed, label_processed = data_preprocesssing(data, label, 128, 64)

# you can type the name of your dataset like: "mhealth.dat" , "pamap2.dat"
target_filename = "pamap2.dat"
obj = [(data_processed, label_processed)]
f = open(os.path.join("data_", target_filename), 'wb')
cp.dump(obj, f, protocol=-1)
f.close()