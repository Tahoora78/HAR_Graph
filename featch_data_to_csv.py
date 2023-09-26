import os
import pandas as pd
import numpy as np


def convert_mhealth_data_to_csv():
    df = pd.DataFrame()
    # loop to combine all data
    for i in range(1, 10):
        df1 = pd.read_csv(f'PAMAP2_Dataset/Protocol/subject10{i}.dat', header=None, sep=' ')
        print(df1)
        df1 = df1.rename(columns={
            1: "Activity"
        })
        df = pd.concat([df, df1])

    # loop to combine all data
    for i in [1, 5, 6, 8, 9]:
        df1 = pd.read_csv(f'PAMAP2_Dataset/Optional/subject10{i}.dat', header=None, sep=' ')
        print(df1)
        df1 = df1.rename(columns={
            1: "Activity"
        })
        df = pd.concat([df, df1])

    # make all labels between 1-18 --> cause we have only 18 activites
    df["Activity"] = df["Activity"].replace(19, 8)
    df["Activity"] = df["Activity"].replace(20, 14)
    df["Activity"] = df["Activity"].replace(24, 15)

    # replace Nan value with mean 
    df = df.replace(np.nan, df.mean())

    # saving the result
    df.to_csv('pamap2_raw_data.csv',index = False)


def convert_mhealth_data_to_csv():
    df = pd.DataFrame()
    # loop to combine all data
    for i in range(1, 10):
        df1 = pd.read_csv(f'MHEALTHDATASET/mHealth_subject{i}.log', header=None, sep='\t')
        df1 = df1.rename(columns={
            23:"Activity"
        })
        df = pd.concat([df, df1])
    # storing result
    df.to_csv('mhealth_raw_data.csv', index = False)


def convert_opportunity_data_to_csv():
    df = pd.DataFrame()
    # loop to combine all data
    for i in range(1, 10):
        df1 = pd.read_csv(f'MHEALTHDATASET/mHealth_subject{i}.log', header=None, sep='\t')
        df1 = df1.rename(columns={
            23:"Activity"
        })
        df = pd.concat([df, df1])
    # storing result
    df.to_csv('mhealth_raw_data.csv', index=False)
