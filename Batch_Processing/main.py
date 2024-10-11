# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 18:58:33 2024

@author: USER
"""

import time
import tkinter as tk
from process import Process
from batch import Batch
from queue import Queue

#Batch size for this program
bS = 2

def windowFormat():
    window = tk.Tk()
    window.title("Operative system")
    window.configure(background="#bab29c")
    window.geometry("720x480")
    return window

def labelFormat(master,text):
    lbl = tk.Label(master, text=text,bg="#bab29c",justify=tk.CENTER, font=(20))
    return lbl

def entryFormat(master,textVariable):
    entry = tk.Entry(master, textvariable = textVariable)
    return entry

window = windowFormat()

txtVar = tk.StringVar()

entVar = None

def submit():
    global entVar
    entVar = int(txtVar.get())
    window.destroy()

lbl = labelFormat(window,"\nHow many operations do you want to process?\n")
lbl.pack()

processEnt = entryFormat(window,txtVar)
processEnt.pack()

lbl = labelFormat(window,"")
lbl.pack()

sub = tk.Button(window,text='Submit', command=submit)
sub.pack()

window.mainloop()

batchQueue = Queue()
auxBatch = Batch(bS)
tmet = 0
tProcesses = entVar
i = 0

#Process capture

while (tProcesses != 0):
    
    window = windowFormat()
    
    auxProcess = Process()
    
    def submit():
        global auxProcess
        auxProcess.name = txtName.get()
        auxProcess.x = int(txtX.get())
        auxProcess.operation = txtOp.get()
        auxProcess.y = int(txtY.get())
        auxProcess.met = int(txtMet.get())
        window.destroy()
    
    txtName = tk.StringVar()
    txtX = tk.StringVar()
    txtOp = tk.StringVar()
    txtId = tk.StringVar()
    txtY = tk.StringVar()
    txtMet = tk.StringVar()
    
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)
    
    lf = tk.LabelFrame(window, text="Process number: " + str(i + 1), padx=20, pady=20, font=(26), bg="#bab29c")
    lf.grid(row=0, column=1, padx=20, pady=20)
    
    lbl = labelFormat(lf,"Process name: ")
    lbl.pack()
    ent1 = entryFormat(lf,txtName)
    ent1.pack()
    lbl = labelFormat(lf,"Operand 1: ")
    lbl.pack()
    ent2 = entryFormat(lf,txtX)
    ent2.pack()
    lbl = labelFormat(lf,"Operation type: ")
    lbl.pack()
    ent3 = entryFormat(lf,txtOp)
    ent3.pack()
    lbl = labelFormat(lf,"Operand 2: ")
    lbl.pack()
    ent4 = entryFormat(lf,txtY)
    ent4.pack()

    auxProcess.pid = i
    
    lbl = labelFormat(lf,"Maximum estimated time: ")
    lbl.pack()
    ent5 = entryFormat(lf,txtMet)
    ent5.pack()
    
    lbl = labelFormat(lf,"")
    lbl.pack()
    
    sub = tk.Button(lf,text='Submit', command=submit)
    sub.pack()
    
    window.mainloop()
    
    #Process enqueue
    
    if(auxBatch.processQueue.full()):     #When reaching batch size, enqueue batch  
        batchQueue.put(auxBatch)
        auxBatch = Batch(bS)
        
    auxBatch.processQueue.put(auxProcess)
        
    i += 1
    tProcesses -= 1 #Decrement remaining processes
        
if(not auxBatch.processQueue.empty()): #Case - Queuing an incomplete batch
    batchQueue.put(auxBatch)


#End of first part    


def update():
    global batchQueue
    global doneArr
    global processArr
    global auxProcess
    global timeT
    global timeE
    global flag
    global lbl00
    global lbl1
    global lbl2
    global lbl3
    global lbl4
    global lbl5
    global lbl6
    global lbl9
    global lbl10
    
    if(not timeT == 0):
            
        if(len(processArr) == 0 and flag == False): #get new batch and fill processArr with current batch processes
            if (not batchQueue.empty()):
                currentBatch = batchQueue.get()
                
                for i in range(currentBatch.processQueue.qsize()):
                    processArr.append(currentBatch.processQueue.get()) 
                    
                auxProcess = processArr[0] #assign process currently being processed
                processArr.pop(0) #pop it from current batch processes array
                timeE = 0
                flag = True
            
        lbl01.config(text="Number of pending batches: " + str(batchQueue.qsize()))
            
        processStr = ""
        for i in processArr:
            processStr = processStr + str(i.name)+ "    " +str(i.met) + "\n"
        lbl00.config(text=processStr)
        
        lbl1.config(text="ID: " + str(auxProcess.pid))
        lbl2.config(text="OP: " + str(auxProcess.operation))
        lbl3.config(text="MET: " + str(auxProcess.met))
        lbl4.config(text="NAME: " + str(auxProcess.name))
        lbl5.config(text="TE: " + str(timeE))
        lbl6.config(text="TR: " + str(auxProcess.met - timeE))
        
        doneStr = ""
        for i in doneArr:  
          doneStr = doneStr + str(i.pid) + "    " + str(i.operation) + "   " + str(i.x) + "\n"
        lbl9.config(text=doneStr)
            
        lbl10.config(text="Total time elapsed: "+str(timeT))
     
        timeE = timeE + 1    
     
        if(timeE == auxProcess.met):
            doneArr.append(auxProcess)          
            if(len(processArr) > 0):
                auxProcess = processArr[0] #assign process currently being processed
                timeE = 0
                processArr.pop(0) #pop it from current batch processes array
                
            else:
                flag = False
    else:
        processArr.pop(0)
        
    timeT = timeT + 1
    
    if(timeE == auxProcess.met + 1):
        lbl1.config(text="ID: ")
        lbl2.config(text="OP: ")
        lbl3.config(text="MET: ")
        lbl4.config(text="NAME: ")
        lbl5.config(text="TE: ")
        lbl6.config(text="TR: ")
        return
        
    window.after(1000, update)
    
displayProcess = Process()
auxProcess = displayProcess
processArr = []
processArr.append(displayProcess)
doneArr = [] #array to store finished processes (it is initialized here because they are permanent)
    
window = windowFormat()

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

timeT = 0
timeE = 0
flag = False
    
#fake left panel


lbl01 = labelFormat(window,"Number of pending batches: " + str(batchQueue.qsize()))
lbl01.grid(row=0, column=1)

lf0 = tk.LabelFrame(window, text="Curret Batch", padx=10, pady=10, font=(26), bg="#bab29c")
lf0.grid(row=1, column=0, padx=20, sticky=tk.NSEW)

lbl02 = labelFormat(lf0, "Name   MET")
lbl02.pack()
    
lbl00 = tk.Label(lf0, text="",bg="#bab29c",justify=tk.CENTER, font=(20))
lbl00.pack() #pending processes


#fake middle panel


lf1 = tk.LabelFrame(window, text="Processing", padx=10, pady=10, font=(26), bg="#bab29c")
lf1.grid(row=1, column=1, padx=20, sticky=tk.NSEW)

lbl1 = tk.Label(lf1, text="",bg="#bab29c", font=(20))
lbl1.pack()
lbl2 = tk.Label(lf1, text="",bg="#bab29c", font=(20))
lbl2.pack()
lbl3 = tk.Label(lf1, text="",bg="#bab29c", font=(20))
lbl3.pack()
lbl4 = tk.Label(lf1, text="",bg="#bab29c", font=(20))
lbl4.pack()
lbl5 = tk.Label(lf1, text="",bg="#bab29c", font=(20))
lbl5.pack()
lbl6 = tk.Label(lf1, text="",bg="#bab29c", font=(20))
lbl6.pack()


#fake right panel


lf2 = tk.LabelFrame(window, text="Done", padx=10, pady=10, font=(26), bg="#bab29c")
lf2.grid(row=1, column=2, padx=20, sticky=tk.NSEW)

lbl7 = labelFormat(lf2,"ID      OP    ANS")
lbl7.pack()

lbl9 = tk.Label(lf2, text="",bg="#bab29c",justify=tk.CENTER, font=(20))
lbl9.pack() #done

lbl10 = tk.Label(window, text="Total time elapsed: 0",bg="#bab29c",justify=tk.CENTER, font=(20))#done
lbl10.grid(row=2, column=2, padx=20)

update()
            
window.mainloop()
    
