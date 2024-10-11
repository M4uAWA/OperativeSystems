# @title Programa 3
"""
Created on Sun Aug 25 18:58:33 2024
PROGRAMA 3
@author: USER
"""

import random
import tkinter as tk
from tkinter import ttk
from process import Process


from ctypes import windll #IMPROVE RESOLUTION
windll.shcore.SetProcessDpiAwareness(1)

def windowFormat():
    window = tk.Tk()
    window.title("Operative system")
    window.configure(background="#000000")
    window.geometry("1080x720")
    return window

def labelFormat(master,text):
    lbl = tk.Label(master, text=text, foreground='#d7c7ff', bg="#000000",justify=tk.CENTER, font=('Century Gothic',12))
    return lbl

def entryFormat(master,textVariable):
    entry = tk.Entry(master, textvariable = textVariable, bg="#e1d7fa", font=('Century Gothic',11, 'bold'),justify=tk.CENTER)
    return entry

def submitC():
    global entVar
    entVar = int(txtVar.get())
    window.destroy()

def createNULLP(auxProcess):
    auxProcess = Process()
    auxProcess.pid = "NULL"
    auxProcess.fullOpe = "NULL"
    auxProcess.met = 7
    auxProcess.te = blockedArr[0].ttb # it will work until (oldest blocked remaining time)
    return auxProcess


#for second program
def processCapture(newArr,tProcesses,operators):
    i = 0
    while (tProcesses != 0):

        auxProcess = Process()

        name = "Process" + str(i+1)
        meOma0 = int(random.randrange(1,2))
        auxProcess.name = name
        auxProcess.pid = i
        auxProcess.x = int(random.randrange(-99,99))
        auxProcess.operation = random.choice(operators)

        if(auxProcess.operation == "/" or auxProcess.operation == "%"):
            if(meOma0 == 1):
                auxProcess.y = int(random.randrange(1,99))
            else:
                auxProcess.y = int(random.randrange(-99,-1))
        else:
            auxProcess.y = int(random.randrange(-99,99))
        auxProcess.met = int(random.randrange(5,25))

        if(auxProcess.operation == "/"):
            auxProcess.result = round(auxProcess.x / auxProcess.y,2)
            auxProcess.fullOpe = str(auxProcess.x) + auxProcess.operation + str(auxProcess.y)

        elif(auxProcess.operation == "%"):
            auxProcess.result = round(auxProcess.x % auxProcess.y,2)
            auxProcess.fullOpe = str(auxProcess.x) + auxProcess.operation + str(auxProcess.y)

        elif(auxProcess.operation == "+"):
            auxProcess.result = round(auxProcess.x + auxProcess.y,2)
            auxProcess.fullOpe = str(auxProcess.x) + auxProcess.operation + str(auxProcess.y)

        elif(auxProcess.operation == "-"):
            auxProcess.result = round(auxProcess.x - auxProcess.y,2)
            auxProcess.fullOpe = str(auxProcess.x) + auxProcess.operation + str(auxProcess.y)

        elif(auxProcess.operation == "*"):
            auxProcess.result = round(auxProcess.x * auxProcess.y,2)
            auxProcess.fullOpe = str(auxProcess.x) + auxProcess.operation + str(auxProcess.y)

        #Process enqueue

        newArr.append(auxProcess)

        i += 1
        tProcesses -= 1 #Decrement remaining processes

    return newArr


#for second program
def updateProgressbar():
    step = progressVar.get()
    step += 1
    if (step > 100):
        window.destroy()
        return
    progressVar.set(step)
    progressBar["value"] = step
    window.after(25, updateProgressbar)


#for second program
def keyHandler(key):
    global auxProcess
    global newArr
    global blockedArr
    global blockedLblArr
    global pauseCondition
    global timeT
    global timeChange
    global maxBlocked

    if(pauseCondition == False):

        if(int(key.keycode) == 69): #ERROR - E
            if(not (auxProcess.pid == "NULL")): #if it's null process, don't do ERROR procedure
                auxProcess.finT = timeT
                auxProcess.result = "ERROR"

                if(timeChange != timeT): #Check if interruption was pressed twice in the same second (prevents decrementing te of a process in readyarr)
                    auxProcess.te = auxProcess.te - 1

                if(len(newArr) > 0): #if there are processes in new, append to ready and set current as oldest in ready
                    doneArr.append(auxProcess)
                    readyArr.append(newArr.pop(0))
                    auxProcess = readyArr.pop(0)#assign process currently being processed

                elif(len(readyArr) > 0): #if there aren't processes in new set current as oldest in ready and decrease blocked maximum capacity
                    maxBlocked -= 1
                    doneArr.append(auxProcess)
                    auxProcess = readyArr.pop(0)#assign process currently being processed

                elif(len(blockedArr) > 0):
                    maxBlocked -= 1
                    doneArr.append(auxProcess)
                    auxProcess = createNULLP(auxProcess)

                else:
                    auxProcess.te = auxProcess.met


        elif(int(key.keycode) == 73): #INTERRUPTION - I

                if(timeChange != timeT): #Check if interruption was pressed twice in the same second (prevents decrementing te of a process in readyarr)
                    auxProcess.te = auxProcess.te - 1

                if(not (len(blockedArr) == maxBlocked)): #while the amount of maximum blocked processes hasn't been reached, continue blocking
                    auxProcess.ttb = 0
                    blockedArr.append(auxProcess) #add new blocked process to the list
                    blckdLbl = tk.Label(lf3, text="",bg="#171717", font=('Consolas',12), foreground='#d7c7ff', padx=10, pady=10, relief="groove", bd=2)
                    blockedLblArr.append(blckdLbl) #add new blocked label to the list

                if(len(blockedArr) == maxBlocked): # If it's been reached, start null process
                    auxProcess = createNULLP(auxProcess)

                if(len(readyArr) > 0):
                    auxProcess = readyArr.pop(0) #If there's still processes in readyArr and current process was blocked, get new form there


        elif(int(key.keycode) == 80): #PAUSE - P
            lf1.config(text="Paused")
            pauseCondition = True
            timeT = timeT - 1
            auxProcess.te = auxProcess.te - 1
            for i in blockedArr:
                i.ttb = i.ttb - 1

    elif(int(key.keycode) == 67): #CONTINUE - C
        if(pauseCondition == True): #don't alter if there were no pauses
            lf1.config(text="Running")
            timeT = timeT + 1
            auxProcess.te = auxProcess.te + 1
            for i in blockedArr:
                i.ttb = i.ttb + 1
            pauseCondition = False

    timeChange = timeT #sets the time at which the interruption was made

    return

def updateProcessing():
    global doneArr
    global newArr
    global readyArr
    global blockedArr
    global blockedLblArr
    global auxProcess
    global timeT
    global maxBlocked
    global pauseCondition


    for i in blockedArr: #iterate in blocked processes
        if(i.ttb == 7): #if a blocked process has reached it's time limit, destroy the label for it
            blockedLblArr.pop(0).destroy()

    for i in range(len(blockedArr) - len(blockedLblArr)): #Get the diference in lenght between blocked labels and blocked processes, and iterate that many times
            readyArr.append(blockedArr.pop(0)) #append list of ready with the processes that have reached their time limit (the oldest ones)

            if(auxProcess.pid == "NULL"): #If there are no processes in ready, automatically set current process (if NULL process was running)
                auxProcess = readyArr.pop(0)

    for i in newArr:
         i.arrT = i.arrT + 1

    for i in readyArr:
         if(not(i.te > 0)):
             i.resT = i.resT +1

    if(auxProcess.te == auxProcess.met):

        auxProcess.finT = timeT
        if(len(newArr) > 0): #if there are processes in new, append to ready and set current as oldest in ready
            doneArr.append(auxProcess)
            readyArr.append(newArr.pop(0))
            auxProcess = readyArr.pop(0)#assign process currently being processed

        elif(len(readyArr) > 0): #if there aren't processes in new set current as oldest in ready and decrease blocked maximum capacity
            maxBlocked -= 1
            doneArr.append(auxProcess)
            auxProcess = readyArr.pop(0)#assign process currently being processed

        else:
            doneArr.append(auxProcess)

    lbl01.config(text="\nNumber of pending New: " + str(len(newArr)))



    processStr = "ID    MET    TE\n"
    for i in readyArr:
        processStr = processStr + str(i.pid).ljust(6) +str(i.met).ljust(7)+str(i.te) +"\n"
    lbl00.config(text=processStr)

    lbl1.config(text="ID: " + str(auxProcess.pid))
    lbl2.config(text="OP: " + str(auxProcess.fullOpe))
    lbl3.config(text="MET: " + str(auxProcess.met))
    lbl5.config(text="TE: " + str(auxProcess.te))
    lbl6.config(text="TR: " + str(auxProcess.met - auxProcess.te))

    doneStr ="ID     OP          ANS\n"
    for i in doneArr:
      doneStr = doneStr + str(i.pid).ljust(7) + str(i.fullOpe).ljust(12) + str(i.result) + "\n"
    lbl9.config(text=doneStr)

    count = 0
    for i in blockedArr: #iterate in blocked list
        blockedLblArr[count].config(text="ID: " + str(i.pid) +"\n" + "TTB: " + str(i.ttb)) #Update values
        blockedLblArr[count].grid(row=0,column=count, padx=15, pady=15) #pack them (show them in the GUI)
        count += 1

    lbl10.config(text="Total time elapsed: " + str(timeT))

    if(pauseCondition == False):

        timeT = timeT + 1

        auxProcess.te = auxProcess.te + 1

        for i in blockedArr: #update time to every process in blocked list
            i.ttb = i.ttb + 1


    if(auxProcess.te == auxProcess.met + 1):
        lbl1.config(text="ID: ")
        lbl2.config(text="OP: ")
        lbl3.config(text="MET: ")
        lbl5.config(text="TE: ")
        lbl6.config(text="TR: ")
        auxProcess.te = auxProcess.te - 1
        return

    window.bind("<Key>", keyHandler) #keypress detection



    window.after(1000, updateProcessing)



#############################################Program start

window = windowFormat()

txtVar = tk.StringVar()
entVar = None

lbl = labelFormat(window,"\n\n\n\nHow many New Processes do you want to generate?\n")
lbl.pack()

processEnt = entryFormat(window,txtVar)
processEnt.pack()

lbl = labelFormat(window,"")
lbl.pack()

sub = tk.Button(window,text='Submit', font=('Century Gothic',11), relief="flat", background='#e1d7fa', command=submitC)
sub.pack()

window.mainloop()


#Process capture

tProcesses = entVar
operators = "+-*/%"
i = 0
newArr = []
readyArr = []

newArr = processCapture(newArr,tProcesses,operators)

if(len(newArr) >= 5):
    maxBlocked = 5 #maximum amount of blocked processes
else:
    maxBlocked = len(newArr)

for i in range(len(newArr)): #set the amount of processes that can be in the system at once
    if(i == 5):
        break
    readyArr.append(newArr.pop(0))

i = 0
window = windowFormat() #generating processes window

lbl = labelFormat(window,"\n\n\n\n\nGenerating New Processes...\n")
lbl.pack()

progressBarSyle = ttk.Style() #progressbar style
progressBarSyle.theme_use('clam')

progressBarSyle.configure("violet.Horizontal.TProgressbar",troughcolor='#000000',background='#d7c7ff',darkcolor="#e1d7fa",lightcolor="#ffffff",bordercolor="#e1d7fa",)

progressVar = tk.DoubleVar()
progressBar = ttk.Progressbar(variable=progressVar,length=250,maximum=100, style="violet.Horizontal.TProgressbar")
progressBar.pack()

updateProgressbar()

window.mainloop()

#End of first part

window = windowFormat()
auxProcess = readyArr.pop(0)
doneArr = [] #array to store finished processes (it is initialized here because they are permanent)
blockedArr = [] #list of blocked processes
blockedLblArr = [] #List of labels for blocked processes

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

timeT = 0
timeChange = 0
pauseCondition = False


#left panel


lbl01 = labelFormat(window,text="")
lbl01.grid(row=0, column=2)

lf0 = tk.LabelFrame(window, text="Ready", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
lf0.grid(row=1, column=0, padx=20, sticky=tk.NSEW)

lbl00 = tk.Label(lf0, text="",bg="#000000", justify=tk.LEFT,font=('Consolas',12), foreground='#d7c7ff')
lbl00.pack() #pending processes


#middle panel


lf1 = tk.LabelFrame(window, text="Running", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
lf1.grid(row=1, column=1, padx=20, sticky=tk.NSEW)

lbl1 = tk.Label(lf1, text="",bg="#000000", font=('Consolas',12), foreground='#d7c7ff')
lbl1.pack(anchor="w")
lbl2 = tk.Label(lf1, text="",bg="#000000", font=('Consolas',12), foreground='#d7c7ff')
lbl2.pack(anchor="w")
lbl3 = tk.Label(lf1, text="",bg="#000000", font=('Consolas',12), foreground='#d7c7ff')
lbl3.pack(anchor="w")
lbl5 = tk.Label(lf1, text="",bg="#000000", font=('Consolas',12), foreground='#d7c7ff')
lbl5.pack(anchor="w")
lbl6 = tk.Label(lf1, text="",bg="#000000", font=('Consolas',12), foreground='#d7c7ff')
lbl6.pack(anchor="w")
lbl7 = tk.Label(lf1, text="",bg="#000000", font=('Consolas',12), foreground='#d7c7ff')
lbl7.pack(anchor="w")


#right panel


lf2 = tk.LabelFrame(window, text="Terminated", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
lf2.grid(row=1, column=2, padx=20, sticky=tk.NSEW)

lbl9 = tk.Label(lf2, text="",bg="#000000",justify=tk.LEFT, font=('Consolas',12), foreground='#d7c7ff')
lbl9.pack() #done

lf3 = tk.LabelFrame(window, text="Blocked", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
lf3.grid(row=2, column=0, padx=20, columnspan=3,sticky=tk.NSEW)

lbl10 = tk.Label(window, text="Total time elapsed: 0",bg="#000000",justify=tk.CENTER, font=('Century Gothic',12), foreground='#d7c7ff')#done
lbl10.grid(row=3, column=2, padx=20)

updateProcessing()

window.mainloop()

#PCB
status = ""
pcbString = "         ID     MET    STA    ArrivalTime     FinalTime     ServiceTime     WaitingTime     ReturnTime     ResponseTime\n"
pcbString2 = ""
for i in doneArr:
    i.servT = i.te
    i.retT = i.finT - i.arrT
    i.waitT = i.retT - i.servT
    if (not(i.result == 'ERROR')):
        status = 'Normal'
    else:
        status = "Error"

    pcbString2 =pcbString2 +  str(i.pid).ljust(8)+ str(i.met).ljust(10) + status + "          " + str(i.arrT).ljust(22) + str(i.finT).ljust(22) + str(i.servT).ljust(22) + str(i.waitT).ljust(22) + str(i.retT).ljust(22) + str(i.resT).ljust(10) + "\n"


window = windowFormat()

lf4 = tk.LabelFrame(window, text="P C B", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
lf4.grid(row=1, column=1, padx=20, sticky=tk.NSEW)

lf5 = tk.LabelFrame(window, text="", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
lf5.grid(row=5, column=1, padx=20, sticky=tk.NSEW)

lblpcb = labelFormat(lf4, text=pcbString)
lblpcb.pack()

lblpcb2 = labelFormat(lf5, text=pcbString2)
lblpcb2.pack()



window.mainloop()