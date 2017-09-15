#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv
with open('A.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    rows= [row for row in reader]

print rows