# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 11:10:14 2018

@author: Administrator
"""

import pandas as pd
import pickle

test_dir = r"C:\Users\Administrator\Desktop\test.csv"
with open(test_dir, 'rb') as f:
    a = pickle.load(f)