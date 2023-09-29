import numpy as np
from sklearn.model_selection import train_test_split
from torch_geometric.data import Data, InMemoryDataset
import torch
from torch_geometric.data import DataLoader
import os
import pandas as pd
import _pickle as cp



def get_dataset(pa = 'data_/mhealth.dat'): #/home/ltz/zhaojj/PAMAP2_Dataset/Protocol
    train, test = gen_dataset(pa)
    return HarTaDataset(save_root="../data_", data=train), HarDataset(save_root="../data_", data=test)


def gen_dataset(path):
    print("Loading data...")
    in_data, label_processed = load_dataset(path)
    X_train, X_test, y_train, y_test = train_test_split(in_data, label_processed, test_size=0.2, random_state=42)
    corrcoef = np.loadtxt(open("data_/adj_mhealth.csv", "rb"), delimiter=",", skiprows=0)
    print("Loading over...")
    return to_graph(X_train, y_train, corrcoef), to_graph(X_test, y_test, corrcoef)


def to_graph(data, label, cor):
    data_ist = []
    edge_index = []
    for i in range(cor.shape[0]):
        for j in range(cor.shape[0]):
            if i != j:
                if abs(cor[i,j]) > 0.2:
                    edge_index.append([i, j])
    edge_index = torch.tensor(edge_index, dtype=torch.long)
    for i in range(data.shape[0]):
        da = data[i, :, :].T
        x = Data(x=torch.tensor(da, dtype=torch.float), edge_index=edge_index.t().contiguous(),
                 y=torch.tensor(label[i]-1, dtype=torch.long))
        data_ist.append(x)
    return data_ist


def load_dataset(filename):
    with open(filename, 'rb') as f:
        data = cp.load(f)

    x = data[0][0]
    y = data[0][1]

    print(" ..from file {}".format(filename))
    print(" ..reading instances: x {0}".format(x.shape))

    X_ = x.astype(np.float32)

    # The targets are casted to int8 for GPU compatibility.
    y = y.astype(np.longlong)
    return X_, y


class HarTaDataset(InMemoryDataset):

    def __init__(self, save_root, transform=None, pre_transform=None, data=None):
        self.d = data
        super(HarTaDataset, self).__init__(save_root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_file_names[0])

    @property
    def raw_file_names(self):
        return ['origin_dataset']

    @property
    def processed_file_names(self):
        return ['har_ta_dataset.pt']

    def download(self):
        pass

    @property
    def process(self):
        # 100 samples
        data, slices = self.collate(self.d)
        torch.save((data, slices), self.processed_file_names[0])

        def pr():
            print("load success")

        return pr


class HarDataset(InMemoryDataset):

    def __init__(self, save_root, transform=None, pre_transform=None, data=None):
        self.d = data
        super(HarDataset, self).__init__(save_root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_file_names[0])

    @property
    def raw_file_names(self):
        return ['origin_dataset']

    @property
    def processed_file_names(self):
        return ['mmhealth_dataset.pt']

    def download(self):
        pass

    @property
    def process(self):
        # 100 samples
        data, slices = self.collate(self.d)
        torch.save((data, slices), self.processed_file_names[0])

        def pr():
            print("load success")

        return pr


if __name__ == '__main__':
    # dataset = gen_dataset(num_nodes=32, num_node_feature=3, num_edges=84)
    train, test = get_dataset()
    print(1)