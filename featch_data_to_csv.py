import os
import pandas as pd
import numpy as np


def convert_pamap2_data_to_csv():
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
    df.to_csv('pamap2_raw_data.csv', index=False)


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
    df.to_csv('mhealth_raw_data.csv', index=False)


def convert_opportunity_data_to_csv():
    def read_files(path):
        df = pd.DataFrame()
        #pick partial data from dataset
        list_of_files = ['dataset/S1-ADL1.dat',
                        'dataset/S1-ADL2.dat',
                        'dataset/S1-ADL3.dat',
                        'dataset/S1-ADL4.dat',
                        'dataset/S2-ADL1.dat',
                        'dataset/S2-ADL2.dat',
                        'dataset/S2-ADL3.dat',
                        'dataset/S2-ADL4.dat',
                        'dataset/S3-ADL1.dat',
                        'dataset/S3-ADL2.dat',
                        'dataset/S3-ADL3.dat',
                        'dataset/S3-ADL4.dat',
                        'dataset/S4-ADL1.dat',
                        'dataset/S4-ADL2.dat',
                        'dataset/S4-ADL3.dat',
                        'dataset/S4-ADL4.dat',                 
                        ]
        list_of_drill = ['dataset/S1-Drill.dat',
                'dataset/S2-Drill.dat',
                'dataset/S3-Drill.dat',
                'dataset/S4-Drill.dat',
            ]
        col_names = []
        with open('col_names', 'r') as f:# a file with all column names was created
            lines = f.read().splitlines()
            for line in lines:
                col_names.append(line)
        print(len(col_names))
        
        dataCollection = pd.DataFrame()
        for i, file in enumerate(list_of_files):            
            procData = pd.read_table(path+file, header=None, sep='\s+')
            print(len(procData.columns))
            # print(procData)
            procData.columns = col_names
            procData['file_index'] = i # put the file index at the end of the row
            dataCollection = pd.concat([dataCollection, procData], ignore_index=True)
        dataCollection.reset_index(drop=True, inplace=True)
        return dataCollection
    path = "./opportunity/OpportunityUCIDataset/"
    df = read_files(path)
    df = df.replace(np.nan, df.mean())
    df = df.rename(columns={'Locomotion': 'Activity'})
    df['Activity'] = df['Activity'].replace(0, 4)
    df['Activity'] = df['Activity'].replace(5, 3)
    df.to_csv('oppo_raw_data.csv',index = False)


if __name__ == "main":
    convert_pamap2_data_to_csv()
    convert_mhealth_data_to_csv()
    convert_opportunity_data_to_csv()