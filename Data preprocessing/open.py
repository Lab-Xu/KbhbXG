#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 08:53:47 2023

@author: chenleqi
"""

import pandas as pd
import re
import warnings
warnings.filterwarnings("ignore")

    
 
def read_txt(filename):
    
    # data = pd.read_table(filename,header=None,delim_whitespace=True,error_bad_lines=False)
    data = pd.read_csv('Butyrylation.csv',header=None)
    data = data.iloc[:,[1,2,6]]
    
    data.rename(columns={1:"Protein",2:"pos",6:"Sequence"},inplace=True)
    return data

def genPos(data,window):
    
    pos = pd.DataFrame(index = data.index, columns = ['Protein','pos','Sequence'])
    for i in range(0,len(data)):
        len_protein = len(data.iloc[i,2])
        pos_num = data.iloc[i,1]
        ori_protein = data.iloc[i,2]
        if (window < pos_num < (len_protein-window)):
            protein = ori_protein[(pos_num-(window+1)):(pos_num+window)]
            pos.iloc[i,0] = data.iloc[i,0]
            pos.iloc[i,1] = pos_num
            pos.iloc[i,2] = protein
        elif (pos_num <= window):
            protein = ori_protein[:(pos_num+window)]
            protein = protein.rjust((2*window+1),'X')
            pos.iloc[i,0] = data.iloc[i,0]
            pos.iloc[i,1] = pos_num
            pos.iloc[i,2] = protein
        else:
            protein = ori_protein[(pos_num-(window+1)):]
            protein = protein.ljust((2*window+1),'X')
            pos.iloc[i,0] = data.iloc[i,0]
            pos.iloc[i,1] = pos_num
            pos.iloc[i,2] = protein
            
    return pos

def genNeg_step1(data,window):
    
    data_neg = data[['Protein','Sequence']]
    data_neg.drop_duplicates(subset=None, keep='first', inplace=True, ignore_index=True)
    
    neg = pd.DataFrame(columns = ['Protein','neg','Sequence'])
    for i in range(0,len(data_neg)):
        neg_protein = pd.DataFrame(columns = ['Protein','neg','Sequence'])
        ID = data_neg.iloc[i,0]
        protein = data_neg.iloc[i,1]
        len_protein = len(protein)
        lysine = 'K'
        neg_pos = [(m.start()+1) for m in re.finditer(lysine,protein)]
        neg_protein['neg'] = neg_pos
        neg_protein['Protein'] = ID
        neg_protein['Sequence'] = protein
        for j in range(0,len(neg_protein)):
            neg_num = neg_protein.iloc[j,1]
            if (window < neg_num < (len_protein-window)):
                protein_neg = protein[(neg_num-(window+1)):(neg_num+window)]
                neg_protein.iloc[j,2] = protein_neg
            elif (neg_num <= window):
                protein_neg = protein[:(neg_num+window)]
                protein_neg = protein_neg.rjust((2*window+1),'X')
                neg_protein.iloc[j,2] = protein_neg
            else:
                protein_neg = protein[(neg_num-(window+1)):]
                protein_neg = protein_neg.ljust((2*window+1),'X')
                neg_protein.iloc[j,2] = protein_neg
        neg = neg.append(neg_protein)
    neg = neg.reset_index(drop=True)
    
    return neg
    
def genNeg_step2(neg,pos):
    
    pos_compare = pos
    pos_compare.rename(columns={'pos':"position"},inplace=True)
    neg_compare = neg
    neg_compare.rename(columns={'neg':"position"},inplace=True)
    neg_compare = neg_compare.append(pos_compare).drop_duplicates(keep=False)
    neg_compare.rename(columns={'position':"neg"},inplace=True)
    neg = neg_compare
    pos.rename(columns={'position':"pos"},inplace=True)
    
    return neg

    


if __name__=="__main__":
    # data = read_txt('Glycation.txt')
    data = pd.read_csv('kubcdhit.csv')
    # data = read_txt('kubcdhit.csv')
    pos = genPos(data,12)
    neg = genNeg_step1(data,12)
    neg = genNeg_step2(neg,pos)
    neg['Label'] = 0
    pos['Label'] = 1
    kbhb21 = pd.concat([pos[['Protein', 'Sequence', 'Label']], neg[['Protein', 'Sequence', 'Label']]], axis=0)
    kbhb21.to_csv('kub25.csv',index=False)


