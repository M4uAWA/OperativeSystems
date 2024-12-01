# @title Programa 7
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 19:52:46 2024

@author: User
"""

import random
import tkinter as tk
from tkinter import ttk
from process import Process


from ctypes import windll #IMPROVE RESOLUTION
windll.shcore.SetProcessDpiAwareness(1)

memorySize = 48
frameSize = 5

def windowFormat():
    window = tk.Tk()
    window.title("Operative System")
    window.configure(background="#000000")
    window.geometry("1080x720+50+50")
    return window

def labelFormat(master,text):
    lbl = tk.Label(master, text=text, foreground='#d7c7ff', bg="#000000",justify=tk.CENTER, font=('Century Gothic',12))
    return lbl

def dataFormat(master,text):
    lbl = tk.Label(master, text=text, bg="#000000", font=('Consolas',12), foreground='#d7c7ff')
    return lbl

def entryFormat(master,textVariable):
    entry = tk.Entry(master, textvariable = textVariable, bg="#e1d7fa", font=('Century Gothic',11, 'bold'),justify=tk.CENTER)
    return entry

def submitC():
    global entVar
    global entVar2
    entVar = int(txtVar.get())
    entVar2 = int(txtVar2.get())
    window.destroy()

def createNULLP(auxProcess):
    auxProcess = Process()
    auxProcess.pid = "NULL"
    auxProcess.fullOpe = "NULL"
    auxProcess.met = 7
    auxProcess.te = blockedArr[0].ttb # it will work until (oldest blocked remaining time)
    auxProcess.quantum = "NULL"
    return auxProcess


#for second program
def processCapture(newArr,tProcesses,operators,idCount):
    while (tProcesses != 0):

        auxProcess = Process()
        name = "Process" + str(idCount+1)
        meOma0 = int(random.randrange(1,2))
        auxProcess.name = name
        auxProcess.pid = idCount+1
        auxProcess.x = int(random.randrange(-99,99))
        auxProcess.operation = random.choice(operators)
        auxProcess.size = int(random.randrange(6,26))

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

        idCount += 1
        tProcesses -= 1 #Decrement remaining processes

    return idCount,newArr


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
    global operators
    global newArr
    global idCount
    global blockedArr
    global blockedLblArr
    global pauseCondition
    global timeT
    global timeChange
    global maxBlocked
    global quantumT

    if(pcbCondition.get()):
        return

    if(pauseCondition == False):

        if(int(key.keycode) == 69): #ERROR - E #DONE
            if(not (auxProcess.pid == "NULL")): #if it's null process, don't do ERROR procedure
                auxProcess.finT = timeT
                auxProcess.result = "ERR"

                if(timeChange != timeT): #Check if interruption was pressed twice in the same second (prevents decrementing te of a process in readyarr)
                    auxProcess.te = auxProcess.te - 1

                if(len(newArr) > 0): #if there are processes in new, append to ready and set current as oldest in ready
                    doneArr.append(auxProcess)
                    clearPages()
                    insertPages()
                    auxProcess = readyArr.pop(0)#assign process currently being processed
                    setProcessingPages()

                elif(len(readyArr) > 0): #if there aren't processes in new set current as oldest in ready and decrease blocked maximum capacity

                    if(len(readyArr) + len(blockedArr) < 5):
                        maxBlocked -= 1

                    doneArr.append(auxProcess)
                    clearPages()
                    auxProcess = readyArr.pop(0)#assign process currently being processed
                    setProcessingPages()

                elif(len(blockedArr) > 0):
                    maxBlocked -= 1
                    doneArr.append(auxProcess)
                    clearPages()
                    auxProcess = createNULLP(auxProcess)

                else:
                    doneArr.append(auxProcess)
                    clearPages()
                    auxProcess = Process()
                    auxProcess.met = 0


        elif(int(key.keycode) == 73): #INTERRUPTION - I #DONE

            if(not (len(blockedArr) == maxBlocked)): #while the amount of maximum blocked processes hasn't been reached, continue blocking

                auxProcess.quantum = 0

                if(timeChange != timeT): #Check if interruption was pressed twice in the same second (prevents decrementing te of a process in readyarr)
                    auxProcess.te = auxProcess.te - 1

                auxProcess.ttb = 0
                blockedArr.append(auxProcess) #add new blocked process to the list
                blckdLbl = tk.Label(lf3, text="",bg="#171717", font=('Consolas',12), foreground='#d7c7ff', padx=10, pady=10, relief="groove", bd=2)
                blockedLblArr.append(blckdLbl) #add new blocked label to the list
                setBlockedPages()

                if(len(blockedArr) == maxBlocked): # If it's been reached, start null process
                    auxProcess = createNULLP(auxProcess)

                elif(len(readyArr) > 0):
                    auxProcess = readyArr.pop(0) #If there's still processes in readyArr and current process was blocked, get new from there
                    setProcessingPages()



        elif(int(key.keycode) == 78): #N -New process #DONE
            idCount,newArr = processCapture(newArr, 1, operators, idCount)

            cmp = insertPages() != "full"

            if (cmp and maxBlocked < 5):
                maxBlocked += 1

            if (cmp and auxProcess.pid == 'NULL'):
                auxProcess = readyArr.pop(0)
                setProcessingPages()

        elif(int(key.keycode) == 80 or int(key.keycode) == 84 or int(key.keycode) == 65): #PAUSE - P #DONE
            lf1.config(text="Paused")
            pauseCondition = True

            if(timeChange != timeT): #Check if interruption was pressed twice in the same second (prevents decrementing te of a process in readyarr)

                timeT = timeT - 1

                auxProcess.te = auxProcess.te - 1

                auxProcess.quantum = auxProcess.quantum - 1

                for i in blockedArr:
                    i.ttb = i.ttb - 1

            if(int(key.keycode) == 84):
                pcbCondition.set(True)
                showPCB(doneArr)

    elif(int(key.keycode) == 67): #CONTINUE - C DONE
        if(pauseCondition == True): #don't alter if there were no pauses
            lf1.config(text="Running")

            if(timeChange != timeT):

                auxProcess.te = auxProcess.te + 1

                for i in blockedArr:
                    i.ttb = i.ttb + 1

                timeT = timeT + 1

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
    global quantum
    global frameFrames
    global memArr
    global frameSize

    count = 0

    for i in range(len(memArray)): #Update frames every second
        units = ""

        #colors
        if(memArray[i]['status'] == -2):  #SO COLOR
            color = "#d7c7ff"
        elif(memArray[i]['status'] == -1):#EMPTY COLOR
            color = "#000000"
        elif(memArray[i]['status'] == 0): #READY COLOR
            color = "#595fff"
        elif(memArray[i]['status'] == 1): #PROCESSING COLOR
            color = "#d9345a"
        elif(memArray[i]['status'] == 2): #BLOCKED COLOR
            color = "#714287"

        if(i%4 == 0):
            count += 1

        for j in range(memArray[i]['used']): #paint used units
            units = units + "█"
        
        pID = memArray[i]["processId"]
        
        if(pID == -1):
            pID = "--"
        else:
            pID = str(pID).zfill(2)
        
        frameFrames[i]["fr"].config(text=str(i).zfill(2) +" pID: "+pID)
        frameFrames[i]["lbl"].config(text= units.ljust(frameSize," "), foreground=color)

    for i in blockedArr: #iterate in blocked processes
        if(i.ttb == 7): #if a blocked process has reached it's time limit, destroy the label for it
            blockedLblArr.pop(0).destroy()

    for i in range(len(blockedArr) - len(blockedLblArr)): #Get the diference in lenght between blocked labels and blocked processes, and iterate that many times
            aux = auxProcess
            auxProcess = blockedArr.pop(0)
            readyArr.append(auxProcess) #append list of ready with the processes that have reached their time limit (the oldest ones)
            setReadyPages()
            auxProcess = aux


            if(auxProcess.pid == "NULL"): #If there are no processes in ready, automatically set current process (if NULL process was running)
                auxProcess = readyArr.pop(0)
                setProcessingPages()

    if(auxProcess.te == auxProcess.met):

        auxProcess.finT = timeT

        if(len(newArr) > 0): #if there are processes in new, append to ready and set current as oldest in ready
            doneArr.append(auxProcess)
            clearPages()
            insertPages()
            auxProcess = readyArr.pop(0)#assign process currently being processed
            setProcessingPages()

        elif(len(readyArr) > 0): #if there aren't processes in new set current as oldest in ready and decrease blocked maximum capacity
            maxBlocked -= 1
            doneArr.append(auxProcess)
            clearPages()
            auxProcess = readyArr.pop(0)#assign process currently being processed
            setProcessingPages()

        else:
            if(auxProcess.met != 0):
                doneArr.append(auxProcess)
                clearPages()

    if(auxProcess.quantum == quantum):
        readyArr.append(auxProcess)
        setReadyPages()
        auxProcess = readyArr.pop(0)
        setProcessingPages()
        auxProcess.quantum = 0

    lbl01.config(text="\nNumber of pending New: " + str(len(newArr)))

    if(len(newArr) > 0):
        pagesndd = newArr[0].size // frameSize
        if(newArr[0].size % 5 > 0):
            pagesndd += 1
        lbl001.config(text="Oldest process in New: "+ str(newArr[0].pid)+"\nNumber of pages needed: "+str(pagesndd))
    else:
        lbl001.config(text="Oldest process in New: NULL\nNumber of pages needed: NULL")

    processStr = "ID    MET    TE\n"
    for i in readyArr:
        processStr = processStr + str(i.pid).ljust(6) +str(i.met).ljust(7)+str(i.te) +"\n"
    lbl00.config(text=processStr)

    lbl1.config(text="ID: " + str(auxProcess.pid))
    lbl2.config(text="OP: " + str(auxProcess.fullOpe))
    lbl3.config(text="MET: " + str(auxProcess.met))
    lbl5.config(text="TE: " + str(auxProcess.te))
    lbl6.config(text="TR: " + str(auxProcess.met - auxProcess.te))
    lbl7.config(text="QT: " + str(auxProcess.quantum))


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
        if(auxProcess.pid != "NULL"):
            auxProcess.quantum = auxProcess.quantum + 1

        for i in readyArr:
             if(not(i.te > 0)):
                 i.resT = i.resT +1

        auxProcess.te = auxProcess.te + 1

        for i in blockedArr: #update time to every process in blocked list
            i.ttb = i.ttb + 1

    if(auxProcess.te == auxProcess.met + 1):
        lbl1.config(text="ID: ")
        lbl2.config(text="OP: ")
        lbl3.config(text="MET: ")
        lbl5.config(text="TE: ")
        lbl6.config(text="TR: ")
        lbl7.config(text="QT: ")
        auxProcess.te = auxProcess.te - 1
        showPCB(doneArr)
        return

    window.bind("<Key>", keyHandler) #keypress detection

    window.after(900, updateProcessing)

def showPCB(doneArr):
    global pauseCondition
    global auxProcess
    global readyArr
    global blockedArr

    executeArr =[]
    if(auxProcess.pid != 'NULL'):
        executeArr.append(auxProcess)

    pcbString = "ID     MET    OPE      ANS";
    pcbString1 = " ArrivTime    FinalTime    ServiceTime    WaitingTime    ReturnTime    ResponseTime    BlockedTime    QuanTime"
    pcbString2,pcbString3,pcbString4,pcbString5,pcbString6,pcbString7,pcbString8,pcbString9,pcbString10,pcbString11 = [""]*10

    for i in newArr:
        pcbString2 = pcbString2 + str(i.pid).ljust(7) + str(i.met).ljust(7) + str (i.fullOpe).ljust(9) + str("---") + "\n"
        pcbString3 = pcbString3  + str("---").ljust(15) + str("N/A").ljust(14) + str("N/A").ljust(15) + str("N/A").ljust(14) + str("N/A").ljust(15) + str("N/A").ljust(15) + str("N/A").ljust(14) + str("N/A") + "\n"

    for i in readyArr:
        i.servT = i.te
        i.waitT = timeT - i.arrT - i.te

        pcbString4 = pcbString4 + str(i.pid).ljust(7) + str(i.met).ljust(7) + str(i.fullOpe).ljust(9) + str('---') +"\n"
        if(i.te > 0):
            pcbString5 = pcbString5  + str(i.arrT).ljust(15) + str('N/A').ljust(14) + str(i.servT).ljust(15) + str(i.waitT).ljust(14) + str('N/A').ljust(15) + str(i.resT).ljust(15) + str("N/A").ljust(14) + str("N/A") + "\n"
        else:
            pcbString5 = pcbString5  + str(i.arrT).ljust(15) + str('N/A').ljust(14) + str(i.servT).ljust(15) + str(i.waitT).ljust(14) + str('N/A').ljust(15) + str('---').ljust(15) + str("N/A").ljust(14) + str("N/A") + "\n"

    for i in executeArr:
        i.servT = i.te
        i.waitT = timeT - i.arrT - i.te

        pcbString6 = pcbString6 + str(i.pid).ljust(7) + str(i.met).ljust(7) + str(i.fullOpe).ljust(9) + str('---')+"\n"
        pcbString7 = pcbString7  + str(i.arrT).ljust(15) + str('N/A').ljust(14) + str(i.servT).ljust(15) + str(i.waitT).ljust(14) + str('N/A').ljust(15) + str(i.resT).ljust(15) + str("N/A").ljust(14) + str(i.quantum).ljust(3)  + "\n"

    for i in blockedArr:
        i.servT = i.te
        i.waitT = timeT - i.arrT - i.te

        pcbString8 = pcbString8 + str(i.pid).ljust(7) + str(i.met).ljust(7) + str(i.fullOpe).ljust(9) + str('---')+"\n"
        pcbString9 = pcbString9  + str(i.arrT).ljust(15) + str('N/A').ljust(14) + str(i.servT).ljust(15) + str(i.waitT).ljust(14) + str('N/A').ljust(15) + str(i.resT).ljust(15) + str(i.ttb).ljust(14) + str("N/A") + "\n"

    for i in doneArr:
        i.servT = i.te
        i.retT = i.finT - i.arrT
        i.waitT = i.retT - i.servT
        pcbString10 = pcbString10 + str(i.pid).ljust(7) + str(i.met).ljust(7) + str (i.fullOpe).ljust(9) + str(i.result)+ "\n"
        pcbString11 = pcbString11  + str(i.arrT).ljust(15) + str(i.finT).ljust(14) + str(i.servT).ljust(15) + str(i.waitT).ljust(14) + str(i.retT).ljust(15) + str(i.resT).ljust(15) + str("N/A").ljust(14) + str("N/A")  + "\n"


    windowPCB = tk.Toplevel(window)
    windowPCB.configure(bg="#000000")
    windowPCB.title("PCB")
    windowPCB.geometry("1930x720")
    windowPCB.resizable(width=False, height=False)

    #Just to get scrollbar to work
    canvas = tk.Canvas(windowPCB, bg="#000000",highlightthickness=0,width=1904, height=720)
    canvas.grid(row=0, column=0, sticky=tk.NSEW)

    #and to make it pretty
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Vertical.TScrollbar",gripcount=0,troughcolor='#000000',background='#d7c7ff',darkcolor="#e1d7fa",lightcolor="#ffffff",bordercolor="#e1d7fa",arrowcolor="#ffffff",arrowsize=26)

    scrollbar = ttk.Scrollbar(windowPCB,orient="vertical", command=canvas.yview,style="Vertical.TScrollbar")
    scrollbar.grid(row=0, column=1, sticky=tk.NS)

    canvas.configure(yscrollcommand=scrollbar.set)

    framePCB = tk.Frame(canvas, bg="#000000")
    framePCB.pack()
    canvas.create_window((0, 0), window=framePCB, anchor="nw")
    #till here

    lf4 = tk.LabelFrame(framePCB, text="P C B", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
    lf4.grid(row=1, column=1, padx=20,pady=10, sticky=tk.NSEW)

    lf5 = tk.LabelFrame(framePCB, text="T I M E S", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
    lf5.grid(row=1, column=2, padx=20,pady=10, sticky=tk.NSEW)

    lblpcb = dataFormat(lf4, text=pcbString)
    lblpcb.pack()

    lblpcb1 = dataFormat(lf5, text=pcbString1)
    lblpcb1.pack()

    if(len(newArr)>0):
        lf6 = tk.LabelFrame(framePCB, text = 'New', padx=10, pady=10, font=('Century Gothic',12),bg="#000000", foreground='#d7c7ff')
        lf6.grid(row=2, column=1, padx=20, pady=20, sticky=tk.NSEW)

        lf7 = tk.LabelFrame(framePCB, text="-", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        lf7.grid(row=2, column=2, padx=20, pady=20 , sticky=tk.NSEW)

        lblpcb2 = dataFormat(lf6, text=pcbString2)
        lblpcb2.pack()

        lblpcb3 = dataFormat(lf7, text=pcbString3)
        lblpcb3.pack()

    if(len(readyArr)>0):
        lf8 = tk.LabelFrame(framePCB, text = 'Ready', padx=10, pady=10, font=('Century Gothic',12),bg="#000000", foreground='#d7c7ff')
        lf8.grid(row=3, column=1, padx=20, pady=20, sticky=tk.NSEW)

        lf9 = tk.LabelFrame(framePCB, text="-", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        lf9.grid(row=3, column=2, padx=20, pady=20 , sticky=tk.NSEW)

        lblpcb2 = dataFormat(lf8, text=pcbString4)
        lblpcb2.pack()

        lblpcb3 = dataFormat(lf9, text=pcbString5)
        lblpcb3.pack()

    if(len(executeArr) > 0 and (executeArr[0].met != executeArr[0].te)):
        lf10 = tk.LabelFrame(framePCB, text = 'Running', padx=10, pady=10, font=('Century Gothic',12),bg="#000000", foreground='#d7c7ff')
        lf10.grid(row=4, column=1, padx=20, pady=20, sticky=tk.NSEW)

        lf11 = tk.LabelFrame(framePCB, text="-", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        lf11.grid(row=4, column=2, padx=20, pady=20, sticky=tk.NSEW)

        lblpcb4 = dataFormat(lf10, text=pcbString6)
        lblpcb4.pack()

        lblpcb5 = dataFormat(lf11, text=pcbString7)
        lblpcb5.pack()
        executeArr.pop(0)

    if(len(blockedArr) > 0):
        lf12 = tk.LabelFrame(framePCB, text = 'Blocked', padx=10, pady=10, font=('Century Gothic',12),bg="#000000", foreground='#d7c7ff')
        lf12.grid(row=5, column=1, padx=20, pady=20, sticky=tk.NSEW)

        lf13 = tk.LabelFrame(framePCB, text='-', padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        lf13.grid(row=5, column=2, padx=20, pady=20, sticky=tk.NSEW)

        lblpcb6 = dataFormat(lf12, text=pcbString8)
        lblpcb6.pack()

        lblpcb7 = dataFormat(lf13, text=pcbString9)
        lblpcb7.pack()

    if(len(doneArr) > 0):
        lf14 = tk.LabelFrame(framePCB, text = 'Terminated', padx=10, pady=10, font=('Century Gothic',12),bg="#000000", foreground='#d7c7ff')
        lf14.grid(row=6, column=1, padx=20, pady=20, sticky=tk.NSEW)

        lf15 = tk.LabelFrame(framePCB, text="-", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        lf15.grid(row=6, column=2, padx=20, pady=20, sticky=tk.NSEW)

        lblpcb8 = dataFormat(lf14, text=pcbString10)
        lblpcb8.pack()

        lblpcb9 = dataFormat(lf15, text=pcbString11)
        lblpcb9.pack()

    framePCB.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def closePCB(key):
        if(int(key.keycode) == 67):
            pcbCondition.set(False)
            keyHandler(key)
            windowPCB.destroy()

    windowPCB.bind("<Destroy>", lambda e: pcbCondition.set(False))

    windowPCB.bind('<Key>',closePCB)


def showMemory():
    global memArray
    global frameFrames
    global memorySize
    global frameSize

    windowMemory = tk.Toplevel()
    windowMemory.configure(bg="#000000")
    windowMemory.title("Memory")
    windowMemory.geometry("660x720+1132+50")
    windowMemory.resizable(width=False, height=False)

    mainFrame = tk.Frame(windowMemory,bg="#000000")
    mainFrame.pack(anchor=tk.CENTER, pady=5)

    count = 0
    frameFrames = []
    for i in range(len(memArray)):
        units = ""

        #colors
        if(memArray[i]['status'] == -2):  #SO COLOR
            color = "#d7c7ff"
        elif(memArray[i]['status'] == -1):#EMPTY COLOR
            color = "#000000"
        elif(memArray[i]['status'] == 0): #READY COLOR
            color = "#595fff"
        elif(memArray[i]['status'] == 1): #PROCESSING COLOR
            color = "#d9345a"
        elif(memArray[i]['status'] == 2): #BLOCKED COLOR
            color = "#714287"

        if(i%5 == 0):
            count += 1

        for j in range(memArray[i]['used']): #paint used units
            units = units + "█"

        lblf = tk.LabelFrame(mainFrame, text = str(i) +" pID: "+str(memArray[i]["processId"]), padx=10, pady=7, font=('Consolas',10),bg="#000000", foreground="#d7c7ff")
        lblf.grid(column=(i)%5,row=count)
        lbl = tk.Label(lblf, text= units.ljust(frameSize," "),bg="#000000", font=('Consolas',9), foreground=color)
        lbl.pack()
        frameFrames.append({"fr":lblf,"lbl":lbl})

    windowMemory.protocol("WM_DELETE_WINDOW",lambda: None)

#########################################
def insertPages():
    global newArr
    global frameSize
    global memArr
    global readyArr
    global timeT

    for i in range(len(newArr)): #set the amount of processes that can be in the system at once
        pages = newArr[0].size // frameSize

        if(newArr[0].size % frameSize > 0): #internal fragmentation case
            pages = pages + 1

        available = [] #array to store the available frames
        for j in range(len(memArray)):
            if(memArray[j]['status'] == -1):
                available.append(j)
                if(len(available) == pages):
                    break

        units = newArr[0].size
        j = 0
        if(len(available) == pages):
            while units >= frameSize:
                memArray[available[j]]['processId'] = newArr[0].pid
                memArray[available[j]]['status'] = 0
                memArray[available[j]]['used'] = frameSize
                units -= frameSize
                j += 1


            if(units > 0): #internal fragmentation case
                memArray[available[j]]['processId'] = newArr[0].pid
                memArray[available[j]]['status'] = 0
                memArray[available[j]]['used'] = units

            newArr[0].arrT = timeT
            readyArr.append(newArr.pop(0))

        else:
            return "full" #full memory

#############################################

def clearPages():
    global auxProcess
    global memArr
    for i in memArray:
        if(i["processId"] == auxProcess.pid):
            i['status'] = -1
            i["processId"] = "--"

def setReadyPages():
    global auxProcess
    global memArr
    for i in memArray:
        if(i["processId"] == auxProcess.pid):
            i['status'] = 0

def setProcessingPages():
    global auxProcess
    global memArr
    for i in memArray:
        if(i["processId"] == auxProcess.pid):
            i['status'] = 1


def setBlockedPages():
    global auxProcess
    global memArr
    for i in memArray:
        if(i["processId"] == auxProcess.pid):
            i['status'] = 2

#############################################Program start

window = windowFormat()

txtVar = tk.StringVar()
txtVar2 = tk.StringVar()
entVar = None
entVar2 = None

lbl = labelFormat(window,"\n\n\n\nHow many New Processes do you want to generate?\n")
lbl.pack()

processEnt = entryFormat(window,txtVar)
processEnt.pack()

lbl = labelFormat(window,"")
lbl.pack()

lbl01 = labelFormat(window,"Quantum time\n")
lbl01.pack()

processEnt1 = entryFormat(window,txtVar2)
processEnt1.pack()

lbl01 = labelFormat(window,"")
lbl01.pack()

sub = tk.Button(window,text='Submit', font=('Century Gothic',11), relief="flat", background='#e1d7fa', command=submitC)
sub.pack()

window.mainloop()

#Process capture

tProcesses = entVar
quantum = entVar2
operators = "+-*/%"
idCount = 0
newArr = []
readyArr = []
timeT = 0

idCount,newArr = processCapture(newArr,tProcesses,operators, idCount)

memArray = []
for i in range(memorySize): #initialize all frames
    memArray.append({'processId':-1,'status':-1,'used':0})

#SO memory space
for i in range(memorySize - 4,memorySize):
    memArray[i]['processId'] = "OS"
    memArray[i]['status'] = -2
    memArray[i]['used'] = frameSize

if(len(newArr) >= 5):
    maxBlocked = 5 #maximum amount of blocked processes
else:
    maxBlocked = len(newArr)

insertPages()

window = windowFormat() #generating processes window

lbl = labelFormat(window,"\n\n\n\n\nGenerating New Processes...\n")
lbl.pack()

progressBarSyle = ttk.Style() #progressbar style
progressBarSyle.theme_use('clam')

progressBarSyle.configure("violet.Horizontal.TProgressbar",troughcolor='#000000',background='#d7c7ff',darkcolor="#e1d7fa",lightcolor="#ffffff",bordercolor="#e1d7fa")

progressVar = tk.DoubleVar()
progressBar = ttk.Progressbar(variable=progressVar,length=250,maximum=100, style="violet.Horizontal.TProgressbar")
progressBar.pack()

updateProgressbar()

window.mainloop()

#End of first part

window = windowFormat()
auxProcess = readyArr.pop(0)

for i in memArray:
    if(i["processId"] == auxProcess.pid):
        i['status'] = 1


doneArr = [] #array to store finished processes (it is initialized here because they are permanent)
blockedArr = [] #list of blocked processes
blockedLblArr = [] #List of labels for blocked processes

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

timeChange = 0
pauseCondition = False
pcbCondition = tk.BooleanVar()
pcbCondition.set(False)

#left panel


lbl01 = labelFormat(window,text="")
lbl01.grid(row=0, column=1)

lbl001 = labelFormat(window,text="")
lbl001.grid(row=0, column=2)

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

showMemory()
updateProcessing()

window.mainloop()