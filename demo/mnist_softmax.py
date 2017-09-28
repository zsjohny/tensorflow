#!/usr/bin/env python
# -*- coding: UTF-8 -*-


# Import data
#from tensorflow.examples.tutorials.mnist import input_data
import input_data
import tensorflow as tf

# mnist = input_data.read_data_sets("Mnist_data/", one_hot=True)
#
# sess = tf.InteractiveSession()

import pandas as pd
import numpy as np

import tensorflow as tf
from  input_data import  DataSet as ds
CSV_COLUMNS = ["customerId", "chanceId", "birthday", "createDate", "registerPlace", "school", "testArea","position", "education", "loginTime", "createtime", "netPayMoney", "couponMoney", "onlinePayType", "orderFromUrl", "webFrom", "location", "createDate(2)", "createDate(3)", "chanceSoruce","flowSource" ,"crmChanceAssignId" ,"communicationStatus", "advisoryStatus", "callTime", "hasAnswer", "majorRemark","startDateTime", "assignFlag", "advisoryStatus(2)", "crmChanceId", "crmChanceAssignId(2)", "createBy","bespeakTime", "crmCommunicationId", "SDATE,TOTALLEN", "AdvisoryStatus"]

#CSV_COLUMNS = ["customerid", "chanceId", "callThinkLogId", "cancelTime", "netPayMoney"]
DEAL_COLUMNS = ["netPayMoney"]
df_train = pd.read_csv('data/shuju2.csv', names=CSV_COLUMNS, skipinitialspace=True, skiprows=1)
df_test = pd.read_csv('data/shuju2.csv', names=CSV_COLUMNS, skipinitialspace=True, skiprows=1)
df_label = pd.read_csv('data/shuju2.csv', names=CSV_COLUMNS, skipinitialspace=True, usecols=DEAL_COLUMNS, skiprows=1)

lists = np.array(df_train)
inputx = lists
label = np.array(df_label)


# start tensorflow interactiveSession
sess = tf.InteractiveSession()
train = ds(inputx, label, dtype=tf.float32)

# Create the model
x = tf.placeholder(tf.float32, [None, 37])
W = tf.Variable(tf.zeros([37, 1]))
b = tf.Variable(tf.zeros([1]))
y = tf.nn.softmax(tf.matmul(x, W) + b)

# Define loss and optimizer
y_ = tf.placeholder(tf.float32, [None, 1])
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# Train
tf.initialize_all_variables().run()

# Test trained model
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

for i in range(1000):
  batch_xs, batch_ys = train.next_batch(1)
  #batch_xs, batch_ys = mnist.train.next_batch(100)
  train_step.run({x: batch_xs, y_: batch_ys})
  if i % 100 == 0:
    train_accuracy = accuracy.eval({x: batch_xs, y_: batch_ys})
    print "step %d, train accuracy %g" % (i, train_accuracy)


print(accuracy.eval({x: batch_xs, y_: batch_ys}))
