#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#1.定义神经网络类型 LSTM全称长短期记忆人工神经网络（Long-Short Term Memory） 暂定
#2。整理数据
#3。导入数据【数据整理需要根据定义神经网络类型】
#4。定义神经网络变量
#5。定义神经网络函数
#6。训练模型
#7。预测模型


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

#定义常量
rnn_unit = 10       #hidden layer units
input_size = 7
output_size = 1
lr=0.0006         #学习率

#——————————————————导入数据——————————————————————
f = open('data/dataset_2.csv')
f = open('data/data.csv')
df = pd.read_csv(f)     #读入数据
data = df.iloc[:,2:10].values  #取第3-10列
