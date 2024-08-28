# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 18:58:33 2024

@author: USER
"""

import os
import time
import copy
from process import Process
from batch import Batch
from queue import Queue

#Batch size for this program
bS = 2

print("How many processes do you want to capture?\n")
tProcesses = int(input("ANS: "))

batchQueue = Queue()

auxBatch = Batch(bS)
tmet = 0

i = 0
while (tProcesses != 0):
        auxProcess = Process()
        print("\nProcess number", i + 1 ,"\n")
        auxProcess.name = input("Process name: ")
        auxProcess.x = int(input("Operand 1: "))
        auxProcess.operation = input("Operation type: ")
        auxProcess.y = int(input("Operand 2: "))
        auxProcess.pid = i
        auxProcess.met = int(input("Maximum estimated time: "))
        tmet += auxProcess.met
        
        #Process enqueue
        
        if(auxBatch.processQueue.full()):     #When reaching batch size, enqueue batch  
            batchQueue.put(auxBatch)
            auxBatch = Batch(bS)
        auxBatch.processQueue.put(auxProcess)
            
        i += 1
        tProcesses -= 1 #Decrement remaining processes
        
if(not auxBatch.processQueue.empty()): #Case - Queuing an incomplete batch
    print("Final Batch completed with spare space")
    batchQueue.put(auxBatch)
    
#End of first part    

while(not batchQueue.empty()):
    showBatch = batchQueue.get()
        #left panel
    while (not showBatch.processQueue.empty()):
        showCurrentbatch = Batch(bS)
        showCurrentbatch = showBatch
        print("\nNumber of pending batches:", batchQueue.qsize())
        print("\n\nCurret Batch\n")
        print("Name   MET")
        while (not showCurrentbatch.processQueue.empty()):
            showProcess = showCurrentbatch.processQueue.get()
            print(showProcess.name,"    ",showProcess.met)
        
        print("\n\nProcessing")
        #middle panel
        showProcess = showBatch.processQueue.get()
        print("\n\nProcessing")
        print("\nID:" ,showProcess.pid)
        print("\nOP:" ,showProcess.operation)
        print("\nMET:" ,showProcess.met)
        print("\nNAME:" ,showProcess.name,"\n")
        for i in range(showProcess.met):
            print("\rTE:",i,"\nTR:",showProcess.met-i)
            tmet -= 1   
            time.sleep(1)
