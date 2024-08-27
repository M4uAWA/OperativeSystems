# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 18:58:33 2024

@author: USER
"""

import os
import time
from process import Process
from batch import Batch
from queue import Queue

#Batch size for this program
bS = 2

print("How many processes do you want to capture?\n")
tProcesses = int(input("ANS: "))

batchQueue = Queue()
auxProcess = Process()
auxBatch = Batch(bS)
tmte = 0

i = 0
while (tProcesses != 0):
        print("\nProcess number", i + 1 ,"\n")
        auxProcess.name = input("Process name: ")
        auxProcess.x = int(input("Operand 1: "))
        auxProcess.operation = input("Operation type: ")
        auxProcess.y = int(input("Operand 2: "))
        auxProcess.pid = i
        auxProcess.mte = int(input("Maximum estimated time: "))
        tmte += auxProcess.mte
        
        auxBatch.processQueue.put(auxProcess) #Process enqueue
        
        if(auxBatch.processQueue.full()): #When reaching batch size, enqueue batch
            print("Batch completed")
            batchQueue.put(auxBatch)
            while (not auxBatch.processQueue.empty()): #Empty auxBatch processQueue (to reuse auxBatch)
                auxBatch.processQueue.get()
            
        i += 1
        tProcesses -= 1 #Decrement remaining processes
        
if(not auxBatch.processQueue.empty()): #Case - Queuing an incomplete batch
    print("Final Batch completed with spare space")
    batchQueue.put(auxBatch)
    
for i in range(tmte):
    print("Tiempo restante: ",tmte)
    tmte -= 1
    time.sleep(1)
    
    
    





        
        