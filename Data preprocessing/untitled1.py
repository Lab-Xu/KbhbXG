#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 17:30:06 2023

@author: chenleqi
"""
import pandas as pd
def read_data(file_path):
    dataset = pd.read_csv(file_path)

    #查看并显示前三条记录
    print(dataset.iloc[0:3,:])
    print('-' * 30)

    #查看样本数和特征数
    print(dataset.shape)
    print('-' * 30)

    return (dataset)

def main():
    dataset=read_data('Butyrylation31.csv')
    with open("kubraw31.txt", "w") as f:
        for i in range(dataset.shape[0]):
            ex='>'+dataset.iloc[i,0]# +'|'+str(dataset.iloc[i,1])#可以将_改成|，这里因为别的需要先改成别的了
            sq=dataset.iloc[i,1]
            #print(ex,sq)

            f.write(ex)
            f.write('\n')
            f.write(sq)
            f.write('\n')
if __name__ == '__main__':
    main()