# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 19:47:53 2024

@author: USER
"""
from queue import Queue

class Batch:
    def __init__(self, batchSize):
        self.processQueue = Queue(batchSize)