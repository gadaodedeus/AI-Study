import pandas as pd 
import matplotlib.pyplot as plt
import re
from hunspell import Hunspell 
import string

def pie_plot(labels, dict_col, title):
    # axis reference
    x = 0
    y = 0
    
    if(len(dict_col.keys()) > 1):   # one plot required (item on dict)
        fig, axs = plt.subplots(ncols=4,nrows=int(len(dict_col.keys())/4)+1)
    else:   # more than one plot (item on dict)
        fig, axs = plt.subplots()

    fig.suptitle(title) # title
    fig.set_size_inches(18.5, 10.5, forward=True)   # fig format
   
    if(len(dict_col.keys()) > 1):   # more than one item on dict
        for i in dict_col.keys():
            axs[y,x].pie([dict_col[i], 1-dict_col[i]], autopct='%1.1f%%')   # autopct = shows data on pie graph
            axs[y,x].set_title(i)
            axs[y,x].legend(loc='upper right', labels=labels)         
            
            # index update
            if(x==3):
                x=0
                y+=1
            x+=1

    else:   # one item on dict
        axs.pie([dict_col['0'], 1-dict_col['0']], autopct='%1.4f%%')
        axs.legend(loc='upper right', labels=labels)   

    plt.show()

def duplicated(df): # rows duplicated
    percent_dupli = df.duplicated().sum()/len(df)
    labels=['Duplicados','Únicos']
    pie_plot(labels, {'0': percent_dupli}, 'Registros Duplicados')

def missing(df, col): # missing values on columns
    dict_col={}
    for i in col:
        percent_mis = df[i].isna().sum()/len(df)
        dict_col[i]=percent_mis
    labels = ['Faltando', 'Completo']
    pie_plot(labels, dict_col, 'Registros Faltantes')

def dtype_columns(df):  # data type on each row
    print(df.dtypes)

def typo_detect(df, col):
    dict_col={}
    
    h = Hunspell('Portuguese (Brazilian)', hunspell_data_dir='dict')
    for i in col:
        typo_count=0    # qtn rows detected with typo
        for j in range(len(df[i])):
            words=df[i][j]  # get words from df
            words=re.sub(r'\W+', ' ', words)    # remove non-alphanumeric stuff -> whitespace
            words=words.split(' ')  # split to list
            print(words)

            for k in range(len(words)): # check each word of sentence
                if(not h.spell(words[k].lower())):  # misspelled
                    typo_count+=1
                    break

        if(len(col) == 1):  # single plot
            dict_col['0']=typo_count/len(df[i])
        else:               # multiples plots
            dict_col[i]=typo_count/len(df[i])

    labels = ['Errado', 'Correto']
    pie_plot(labels, dict_col, 'Typo Errors')
                

