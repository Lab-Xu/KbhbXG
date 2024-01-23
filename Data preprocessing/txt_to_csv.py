#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 23:57:34 2023

@author: chenleqi
"""

import pandas as pd
import textwrap

def Txt2Csv(Txt_path, Csv_path):
    '''
    :param Txt_path: txt文件路径
    :param Csv_path: csv文件路径
    :return:
    '''
    with open(Txt_path, encoding='utf-8') as f:
        contents = []
        readlines = f.readlines()   # readlines是一个列表
        for i in readlines:
            line = i.strip().split(" ")     # 去掉前后的换行符，之后按逗号分割开
            contents.append(line)   # contents二维列表
    df = pd.DataFrame(contents)

    df.to_csv(Csv_path, header=False)           # 不添加表头
    #df.columns = ["Source", "Target", "Type", "Path"]  # 添加表头
    df.to_csv("Butyrylation.csv", index=False)
    print("数据写入成功")


def read_txt(filename):
    
    # data = pd.read_table(filename,header=None,delim_whitespace=True,error_bad_lines=False)
    data = pd.read_csv('Butyrylation.csv',header=None)
    data = data.iloc[:,[1,2,6]]
    data.rename(columns={1:"Protein",2:"pos",6:"Sequence"},inplace=True)
    return data

def read_data(file_path):
    dataset = pd.read_csv(file_path)

    #查看并显示前三条记录
    print(dataset.iloc[0:3,:])
    print('-' * 30)

    #查看样本数和特征数
    print(dataset.shape)
    print('-' * 30)




def main():
    dataset=read_txt('Butyrylation.txt')
    with open("Butyrylation.txt", "w") as f:
        for i in range(dataset.shape[0]):
            ex='>'+dataset.iloc[i,0]+'|'+str(dataset.iloc[i,1])#可以将_改成|，这里因为别的需要先改成别的了
            wrapped_text = textwrap.wrap(dataset.iloc[i,2], width=70)
            #sq=dataset.iloc[i,2]
            #print(ex,sq)

            f.write(ex)
            f.write('\n')
            for line in wrapped_text:
                f.write(line + '\n')




# 读取txt文件
with open('kubcdhit.fasta.txt', 'r') as f:
    text = f.read()

# 将字符串转换为pandas.Series对象
series = pd.Series(text.split("\n"))

# 筛选以>开头的行，并去掉>
series = series[series.str.startswith(">")].str.replace(">", "")

# 将筛选后的数据转换成DataFrame
df = pd.DataFrame({"Protein": series})
  
df = df.reset_index(drop=True)

data = read_txt('Butyrylation.txt')
    
merged_df = pd.merge(df, data, on='Protein')

merged_df.to_csv('kubcdhit.csv',index=False)   
    
    
    
    
    
