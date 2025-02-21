# @title Programa 4 OOP FINAL
import random
import tkinter as tk
from tkinter import ttk
from process import Process
from queue import Queue
from ctypes import windll  # IMPROVE RESOLUTION

windll.shcore.SetProcessDpiAwareness(1)

class OperativeSystemApp:
    def __init__(self):
        # initial config
        self.entVar = None

        # processing variables
        self.tNew = None
        self.idCount = 0
        self.operators = "+-*/%"
        self.processArr = []
        self.doneArr = []
        self.newArr = []
        self.readyArr = []
        self.blockedArr = []
        self.blockedLblArr = []
        self.timeT = 0
        self.timeChange = 0
        self.flag = False
        self.batchCounter = 0
        self.pauseCondition = False
        self.pcbCondition = False
        self.auxProcess = Process()
        self.processArr.append(self.auxProcess)

        self.operate() #start program

    def operate(self):
        self.mainWindow()
        self.loadingWindowM()
        self.processingWindowM()
        

    def windowFormat(self):
        window = tk.Tk()
        window.title("Operative System")
        window.configure(background="#000000")
        window.geometry("1080x720")
        return window

    def labelFormat(self, master, text):
        lbl = tk.Label(master, text=text, foreground='#d7c7ff', bg="#000000", justify=tk.CENTER, font=('Century Gothic', 12))
        return lbl

    def entryFormat(self, master, textVariable):
        entry = tk.Entry(master, textvariable=textVariable, bg="#e1d7fa", font=('Century Gothic', 11, 'bold'), justify=tk.CENTER)
        return entry
    
    def dataFormat(self, master, text):
        lbl = tk.Label(master, text=text, bg="#000000", font=('Consolas',12), foreground='#d7c7ff')
        return lbl

    def submitC(self):
        self.entVar = int(self.txtVar.get())
        self.window.destroy()
        self.tNew = self.entVar
        
    def createNULLP(self,auxProcess):
        self.auxProcess = Process()
        self.auxProcess.pid = "NULL"
        self.auxProcess.fullOpe = "NULL"
        self.auxProcess.met = 7
        self.auxProcess.te = self.blockedArr[0].ttb # it will work until (oldest blocked remaining time)
        return self.auxProcess

    def processCapture(self):

        while (self.tNew != 0):
            self.idCount += 1
            currentProcess = Process()
            meOma0 = int(random.randrange(1,2))
            currentProcess.pid = self.idCount
            currentProcess.x = int(random.randrange(-99,99))
            currentProcess.operation = random.choice(self.operators)

            if(currentProcess.operation == "/" or currentProcess.operation == "%"):
                if(meOma0 == 1):
                    currentProcess.y = int(random.randrange(1,99))
                else:
                    currentProcess.y = int(random.randrange(-99,-1))
            else:
                currentProcess.y = int(random.randrange(-99,99))
            currentProcess.met = int(random.randrange(5,25))

            if(currentProcess.operation == "/"):
                currentProcess.result = round(currentProcess.x / currentProcess.y,2)
                currentProcess.fullOpe = str(currentProcess.x) + currentProcess.operation + str(currentProcess.y)

            elif(currentProcess.operation == "%"):
                currentProcess.result = round(currentProcess.x % currentProcess.y,2)
                currentProcess.fullOpe = str(currentProcess.x) + currentProcess.operation + str(currentProcess.y)

            elif(currentProcess.operation == "+"):
                currentProcess.result = round(currentProcess.x + currentProcess.y,2)
                currentProcess.fullOpe = str(currentProcess.x) + currentProcess.operation + str(currentProcess.y)

            elif(currentProcess.operation == "-"):
                currentProcess.result = round(currentProcess.x - currentProcess.y,2)
                currentProcess.fullOpe = str(currentProcess.x) + currentProcess.operation + str(currentProcess.y)

            elif(currentProcess.operation == "*"):
                currentProcess.result = round(currentProcess.x * currentProcess.y,2)
                currentProcess.fullOpe = str(currentProcess.x) + currentProcess.operation + str(currentProcess.y)

            #Process enqueue

            self.newArr.append(currentProcess)

            
            self.tNew -= 1 #Decrement remaining processes
        
    def mainWindow(self):
        self.window = self.windowFormat()
        lbl = self.labelFormat(self.window, "\n\n\n\nHow many operations do you want to process?\n")
        lbl.pack()

        self.txtVar = tk.StringVar()

        processEnt = self.entryFormat(self.window, self.txtVar)
        processEnt.pack()

        lbl = self.labelFormat(self.window, "")
        lbl.pack()

        sub = tk.Button(self.window, text='Submit', font=('Century Gothic', 11), relief="flat", background='#e1d7fa', command=self.submitC)
        sub.pack()
        self.window.mainloop()

    def loadingWindowM(self):

        self.processCapture()

        self.loadingWindow = self.windowFormat() #generating processes window

        self.lbl = self.labelFormat(self.loadingWindow,"\n\n\n\n\nGenerating New Processes...\n")
        self.lbl.pack()

        self.progressBarSyle = ttk.Style() #progressbar style
        self.progressBarSyle.theme_use('clam')

        self.progressBarSyle.configure("violet.Horizontal.TProgressbar",troughcolor='#000000',background='#d7c7ff',darkcolor="#e1d7fa",lightcolor="#ffffff",bordercolor="#e1d7fa",)

        self.progressVar = tk.DoubleVar()

        self.progressBar = ttk.Progressbar(variable=self.progressVar,length=250,maximum=100, style="violet.Horizontal.TProgressbar")
        self.progressBar.pack()

        self.updateProgressbar()

        self.loadingWindow.mainloop()

    def updateProgressbar(self):
        step = self.progressVar.get()
        step += 1
        if step > 100:
            self.loadingWindow.destroy()
            return
        self.progressVar.set(step)
        self.progressBar["value"] = step
        self.loadingWindow.after(40, self.updateProgressbar)

    def processingWindowM(self):
        self.processingWindow = self.windowFormat()
        self.readyArr = []
        self.doneArr = [] #array to store finished processes (it is initialized here because they are permanent)
        
        i = 0
        if(len(self.newArr) >= 5):
            self.maxBlocked = 5 #maximum amount of blocked processes
        else:
            self.maxBlocked = len(self.newArr)

        for i in range(len(self.newArr)): #set the amount of processes that can be in the system at once
            if(i == 5):
                break
            self.readyArr.append(self.newArr.pop(0))
            
        self.auxProcess = self.readyArr.pop(0)

        self.processingWindow.columnconfigure(0, weight=1)
        self.processingWindow.columnconfigure(1, weight=1)
        self.processingWindow.columnconfigure(2, weight=1)

        self.timeT = 0
        self.flag = False
        self.pauseCondition = False
        #left panel

        self.lbl01 = self.labelFormat(self.processingWindow,"\nNumber of pending New: " + str(len(self.newArr)))
        self.lbl01.grid(row=0, column=2)

        self.lf0 = tk.LabelFrame(self.processingWindow, text="Ready", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        self.lf0.grid(row=1, column=0, padx=20, sticky=tk.NSEW)

        self.lbl02 = self.labelFormat(self.lf0, "ID   MET    TE")
        self.lbl02.pack()

        self.lbl00 = tk.Label(self.lf0, text="",bg="#000000",justify=tk.CENTER, font=('Century Gothic',12), foreground='#d7c7ff')
        self.lbl00.pack() #pending processes


        #middle panel


        self.lf1 = tk.LabelFrame(self.processingWindow, text="Running", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        self.lf1.grid(row=1, column=1, padx=20, sticky=tk.NSEW)

        self.lbl1 = tk.Label(self.lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
        self.lbl1.pack(anchor="w")
        self.lbl2 = tk.Label(self.lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
        self.lbl2.pack(anchor="w")
        self.lbl3 = tk.Label(self.lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
        self.lbl3.pack(anchor="w")
        self.lbl4 = tk.Label(self.lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
        self.lbl4.pack(anchor="w")
        self.lbl5 = tk.Label(self.lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
        self.lbl5.pack(anchor="w")



        #right panel


        self.lf2 = tk.LabelFrame(self.processingWindow, text="Terminated", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        self.lf2.grid(row=1, column=2, padx=20, sticky=tk.NSEW)

        self.lbl7 = self.labelFormat(self.lf2,"ID      OP    ANS")
        self.lbl7.pack()
        
        self.lf3 = tk.LabelFrame(self.processingWindow, text="Blocked", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        self.lf3.grid(row=2, column=0, padx=20, columnspan=3,sticky=tk.NSEW)
        
        self.lbl9 = tk.Label(self.lf2, text="",bg="#000000",justify=tk.CENTER, font=('Century Gothic',12), foreground='#d7c7ff')
        self.lbl9.pack() #done

        self.lbl10 = tk.Label(self.processingWindow, text="Total time elapsed: 0",bg="#000000",justify=tk.CENTER, font=('Century Gothic',12), foreground='#d7c7ff')#done
        self.lbl10.grid(row=3, column=2, padx=20)

        self.updateProcessing()

        self.processingWindow.mainloop()

    def keyHandler(self, key):
        
        if self.pcbCondition:
            return
        
        if self.pauseCondition == False:
            if int(key.keycode) == 69:  # ERROR - E
                if(not (self.auxProcess.pid == "NULL")): #if it's null process, don't do ERROR procedure
                    self.auxProcess.finT = self.timeT
                    self.auxProcess.result = "ERROR"

                    if(self.timeChange != self.timeT): #Check if interruption was pressed twice in the same second (prevents decrementing te of a process in readyarr)
                        self.auxProcess.te = self.auxProcess.te - 1

                    if(len(self.newArr) > 0): #if there are processes in new, append to ready and set current as oldest in ready
                        self.doneArr.append(self.auxProcess)
                        self.tAuxProcess = self.newArr.pop(0)
                        self.tAuxProcess.arrT = self.timeT
                        self.readyArr.append(self.tAuxProcess)
                        self.auxProcess = self.readyArr.pop(0)#assign process currently being processed

                    elif(len(self.readyArr) > 0): #if there aren't processes in new set current as oldest in ready and decrease blocked maximum capacity
                        self.maxBlocked -= 1
                        self.doneArr.append(self.auxProcess)
                        self.auxProcess = self.readyArr.pop(0)#assign process currently being processed

                    elif(len(self.blockedArr) > 0):
                        self.maxBlocked -= 1
                        self.doneArr.append(self.auxProcess)
                        self.auxProcess = self.createNULLP(self.auxProcess)

                    else:
                        self.doneArr.append(self.auxProcess)
                        self.auxProcess = Process()
                        self.auxProcess.met = 0
                        

            elif int(key.keycode) == 73:  # INTERRUPTION - I
               if(self.timeChange != self.timeT): #Check if interruption was pressed twice in the same second (prevents decrementing te of a process in readyarr)
                   self.auxProcess.te = self.auxProcess.te - 1

               if(not (len(self.blockedArr) == self.maxBlocked)): #while the amount of maximum blocked processes hasn't been reached, continue blocking
                   self.auxProcess.ttb = 0
                   self.blockedArr.append(self.auxProcess) #add new blocked process to the list
                   self.blckdLbl = tk.Label(self.lf3, text="",bg="#171717", font=('Consolas',12), foreground='#d7c7ff', padx=10, pady=10, relief="groove", bd=2)
                   self.blockedLblArr.append(self.blckdLbl) #add new blocked label to the list

               if(len(self.blockedArr) == self.maxBlocked): # If it's been reached, start null process
                   self.auxProcess = self.createNULLP(self.auxProcess)

               if(len(self.readyArr) > 0):
                   self.auxProcess = self.readyArr.pop(0) #If there's still process currently being processed and pop previous process from current batch process array
            
            elif int(key.keycode) == 78:  # NEW - N
                self.tNew = 1
                self.processCapture()

                
                if (self.maxBlocked < 5):
                    self.tAuxProcess = self.newArr.pop(0)
                    self.tAuxProcess.arrT = self.timeT
                    self.readyArr.append(self.tAuxProcess)
                    self.maxBlocked += 1
                    
                if (self.auxProcess.pid == 'NULL' and len(self.blockedArr) != self.maxBlocked):
                    self.auxProcess = self.readyArr.pop(0)
                   

            elif(int(key.keycode) == 80 or int(key.keycode) == 84):  # PAUSE - P
                self.lf1.config(text="Paused")
                self.pauseCondition = True
                
                if(self.timeChange != self.timeT):
                    self.timeT -= 1
                    self.auxProcess.te -= 1
                    for i in self.blockedArr:
                        i.ttb = i.ttb - 1
                
                if(int(key.keycode) == 84):
                   self.pcbCondition=True
                   self.showPCB()

        if int(key.keycode) == 67:  # CONTINUE - C
            if(self.pauseCondition == True): #don't alter if there were no pauses
                self.lf1.config(text="Running")
                if(self.timeChange != self.timeT):
                    self.timeT = self.timeT + 1
                    self.auxProcess.te = self.auxProcess.te + 1
                    for i in self.blockedArr:
                        i.ttb = i.ttb + 1
                self.pauseCondition = False
        
        self.timeChange = self.timeT #sets the time at which the interruption was made

    def showPCB(self):
        self.windowPCB = tk.Toplevel(self.processingWindow)
        self.windowPCB.geometry("1908x720")
        self.windowPCB.configure(bg="#000000")
        self.windowPCB.resizable(width=False, height=False)
        
        #Just to get scrollbar to work
        self.canvas = tk.Canvas(self.windowPCB, bg="#000000",highlightthickness=0,width=1884, height=720 )
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        
        #and to make it pretty
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Vertical.TScrollbar",gripcount=0,troughcolor='#000000',background='#d7c7ff',darkcolor="#e1d7fa",lightcolor="#ffffff",bordercolor="#e1d7fa",arrowcolor="#ffffff",arrowsize=26)
    
        self.scrollbar = ttk.Scrollbar(self.windowPCB,orient="vertical", command=self.canvas.yview,style="Vertical.TScrollbar")
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
    
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
    
        self.framePCB = tk.Frame(self.canvas, bg="#000000")
        self.canvas.create_window((0, 0), window=self.framePCB, anchor="nw")
    
        self.pcbString = "ID     MET    OPE      ANS";
        self.pcbString1 = " ArrivalTime     FinalTime     ServiceTime     WaitingTime     ReturnTime     ResponseTime     BlockedTime"
        self.pcbString2,self.pcbString3,self.pcbString4,self.pcbString5,self.pcbString6,self.pcbString7,self.pcbString8,self.pcbString9,self.pcbString10,self.pcbString11 = [""]*10
        
        self.executeArr =[]
        if(self.auxProcess.pid != 'NULL'):
            self.executeArr.append(self.auxProcess)
        
        self.lf4 = tk.LabelFrame(self.framePCB, text="P C B", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        self.lf4.grid(row=1, column=1, padx=20,pady=10, sticky=tk.NSEW)
        
        self.lf5 = tk.LabelFrame(self.framePCB, text="T I M E S", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        self.lf5.grid(row=1, column=2, padx=20,pady=10, sticky=tk.NSEW)
        
        self.lblpcb = self.dataFormat(self.lf4, text=self.pcbString)
        self.lblpcb.pack() 
        self.lblpcb1 = self.dataFormat(self.lf5, text=self.pcbString1)
        self.lblpcb1.pack()
        
        for i in self.newArr:
            self.pcbString2 = self.pcbString2 + str(i.pid).ljust(7) + str(i.met).ljust(7) + str (i.fullOpe).ljust(9) + str("---") + "\n"
            self.pcbString3 = self.pcbString3  + str("---").ljust(15) + str("N/A").ljust(15) + str("N/A").ljust(15) + str("N/A").ljust(15) + str("N/A").ljust(16) + str("N/A").ljust(18) + str("N/A") + "\n"

        for i in self.readyArr:
            i.servT = i.te
            i.waitT = self.timeT - i.arrT - i.te
    
            self.pcbString4 = self.pcbString4 + str(i.pid).ljust(7) + str(i.met).ljust(7) + str(i.fullOpe).ljust(9) + str('---') +"\n"
            if(i.te > 0):
                self.pcbString5 = self.pcbString5  + str(i.arrT).ljust(15) + str('N/A').ljust(15) + str(i.servT).ljust(15) + str(i.waitT).ljust(15) + str('N/A').ljust(16) + str(i.resT).ljust(18) + str("N/A")+ "\n"
            else:
                self.pcbString5 = self.pcbString5  + str(i.arrT).ljust(15) + str('N/A').ljust(15) + str(i.servT).ljust(15) + str(i.waitT).ljust(15) + str('N/A').ljust(16) + str('---').ljust(18) + str("N/A")+ "\n"
                
        for i in self.executeArr:
            i.servT = i.te
            i.waitT = self.timeT - i.arrT - i.te
    
            self.pcbString6 = self.pcbString6 + str(i.pid).ljust(7) + str(i.met).ljust(7) + str(i.fullOpe).ljust(9) + str('---')+"\n"
            self.pcbString7 = self.pcbString7  + str(i.arrT).ljust(15) + str('N/A').ljust(15) + str(i.servT).ljust(15) + str(i.waitT).ljust(15) + str('N/A').ljust(16) + str(i.resT).ljust(18) + str("N/A")+ "\n"

        for i in self.blockedArr:
            i.servT = i.te
            i.waitT = self.timeT - i.arrT - i.te
    
            self.pcbString8 = self.pcbString8 + str(i.pid).ljust(7) + str(i.met).ljust(7) + str(i.fullOpe).ljust(9) + str('---')+"\n"
            self.pcbString9 = self.pcbString9  + str(i.arrT).ljust(15) + str('N/A').ljust(15) + str(i.servT).ljust(15) + str(i.waitT).ljust(15) + str('N/A').ljust(16) + str(i.resT).ljust(18) + str(i.ttb) + "\n"

        for i in self.doneArr:
            if(i.pid != None):
                i.servT = i.te
                i.retT = i.finT - i.arrT
                i.waitT = i.retT - i.servT
                self.pcbString10 = self.pcbString10 + str(i.pid).ljust(7) + str(i.met).ljust(7) + str (i.fullOpe).ljust(9) + str(i.result)+ "\n"
                self.pcbString11 = self.pcbString11  + str(i.arrT).ljust(15) + str(i.finT).ljust(15) + str(i.servT).ljust(15) + str(i.waitT).ljust(15) + str(i.retT).ljust(16) + str(i.resT).ljust(18) + str("N/A") + "\n"
        
        if(len(self.newArr)>0):
            self.lf6 = tk.LabelFrame(self.framePCB, text = 'New', padx=10, pady=10, font=('Century Gothic',12),bg="#000000", foreground='#d7c7ff')
            self.lf6.grid(row=2, column=1, padx=20, pady=20, sticky=tk.NSEW)
    
            self.lf7 = tk.LabelFrame(self.framePCB, text="-", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
            self.lf7.grid(row=2, column=2, padx=20, pady=20 , sticky=tk.NSEW)
    
            self.lblpcb2 = self.dataFormat(self.lf6, text=self.pcbString2)
            self.lblpcb2.pack()
    
            self.lblpcb3 = self.dataFormat(self.lf7, text=self.pcbString3)
            self.lblpcb3.pack()

        if(len(self.readyArr)>0):
                self.lf8 = tk.LabelFrame(self.framePCB, text = 'Ready', padx=10, pady=10, font=('Century Gothic',12),bg="#000000", foreground='#d7c7ff')
                self.lf8.grid(row=3, column=1, padx=20, pady=20, sticky=tk.NSEW)
        
                self.lf9 = tk.LabelFrame(self.framePCB, text="-", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
                self.lf9.grid(row=3, column=2, padx=20, pady=20 , sticky=tk.NSEW)
        
                self.lblpcb2 = self.dataFormat(self.lf8, text=self.pcbString4)
                self.lblpcb2.pack()
        
                self.lblpcb3 = self.dataFormat(self.lf9, text=self.pcbString5)
                self.lblpcb3.pack()
    
        if(len(self.executeArr) > 0 and (self.executeArr[0].met != self.executeArr[0].te)):
                self.lf10 = tk.LabelFrame(self.framePCB, text = 'Running', padx=10, pady=10, font=('Century Gothic',12),bg="#000000", foreground='#d7c7ff')
                self.lf10.grid(row=4, column=1, padx=20, pady=20, sticky=tk.NSEW)
        
                self.lf11 = tk.LabelFrame(self.framePCB, text="-", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
                self.lf11.grid(row=4, column=2, padx=20, pady=20, sticky=tk.NSEW)
        
                self.lblpcb4 = self.dataFormat(self.lf10, text=self.pcbString6)
                self.lblpcb4.pack()
        
                self.lblpcb5 = self.dataFormat(self.lf11, text=self.pcbString7)
                self.lblpcb5.pack()
                self.executeArr.pop(0)
    
        if(len(self.blockedArr) > 0):
                self.lf12 = tk.LabelFrame(self.framePCB, text = 'Blocked', padx=10, pady=10, font=('Century Gothic',12),bg="#000000", foreground='#d7c7ff')
                self.lf12.grid(row=5, column=1, padx=20, pady=20, sticky=tk.NSEW)
        
                self.lf13 = tk.LabelFrame(self.framePCB, text='-', padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
                self.lf13.grid(row=5, column=2, padx=20, pady=20, sticky=tk.NSEW)
        
                self.lblpcb6 = self.dataFormat(self.lf12, text=self.pcbString8)
                self.lblpcb6.pack()
        
                self.lblpcb7 = self.dataFormat(self.lf13, text=self.pcbString9)
                self.lblpcb7.pack()
    
        if(len(self.doneArr) > 0):
                self.lf14 = tk.LabelFrame(self.framePCB, text = 'Terminated', padx=10, pady=10, font=('Century Gothic',12),bg="#000000", foreground='#d7c7ff')
                self.lf14.grid(row=6, column=1, padx=20, pady=20, sticky=tk.NSEW)
        
                self.lf15 = tk.LabelFrame(self.framePCB, text="-", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
                self.lf15.grid(row=6, column=2, padx=20, pady=20, sticky=tk.NSEW)
        
                self.lblpcb8 = self.dataFormat(self.lf14, text=self.pcbString10)
                self.lblpcb8.pack()
        
                self.lblpcb9 = self.dataFormat(self.lf15, text=self.pcbString11)
                self.lblpcb9.pack()
        
        self.framePCB.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        def closePCB(key):
            if(int(key.keycode) == 67):
                self.pcbCondition=False
                self.keyHandler(key)
                self.windowPCB.destroy()
    
        self.windowPCB.bind("<Destroy>", lambda e: setattr(self, 'pcbCondition', False))
    
        self.windowPCB.bind('<Key>',closePCB)
    
    def updateProcessing(self):
        
        for i in self.blockedArr:
            if(i.ttb == 7):
                self.blockedLblArr.pop(0).destroy()
                
        for i in range(len(self.blockedArr) - len(self.blockedLblArr)): #Get the diference in lenght between blocked labels and blocked processes, and iterate that many times
                self.readyArr.append(self.blockedArr.pop(0)) #append list of ready with the processes that have reached their time limit (the oldest ones)

                if(self.auxProcess.pid == "NULL"): #If there are no processes in ready, automatically set current process (if NULL process was running)
                    self.auxProcess = self.readyArr.pop(0)
        
        if(self.auxProcess.te == self.auxProcess.met):
            
            self.auxProcess.finT = self.timeT
                
            if(len(self.newArr) > 0):
                self.doneArr.append(self.auxProcess)
                self.tAuxProcess = self.newArr.pop(0)
                self.tAuxProcess.arrT = self.timeT
                self.readyArr.append(self.tAuxProcess)
                self.auxProcess = self.readyArr.pop(0)#assign process currently being processed

                
            elif(len(self.readyArr) > 0):
                self.maxBlocked -= 1
                self.doneArr.append(self.auxProcess)
                self.auxProcess = self.readyArr[0] #assign process currently being processed
                self.readyArr.pop(0) #pop it from current batch processes array

            else:
                self.flag = False
                self.doneArr.append(self.auxProcess)


        self.lbl01.config(text="\nNumber of pending New: " + str(len(self.newArr)))

        self.processStr = ""
        for i in self.readyArr:
            self.processStr = self.processStr + str(i.pid)+ "    " +str(i.met) + "    " +str(i.te) +"\n"
        self.lbl00.config(text=self.processStr)

        self.lbl1.config(text="ID: " + str(self.auxProcess.pid))
        self.lbl2.config(text="OP: " + str(self.auxProcess.fullOpe))
        self.lbl3.config(text="MET: " + str(self.auxProcess.met))
        self.lbl4.config(text="TE: " + str(self.auxProcess.te))
        self.lbl5.config(text="TR: " + str(self.auxProcess.met - self.auxProcess.te))

        doneStr =""
        for i in self.doneArr:
            if(i.pid != None):
                doneStr = doneStr + str(i.pid) + "    " + str(i.fullOpe) + "   " + str(i.result) + "\n"
        self.lbl9.config(text=doneStr)

        self.lbl10.config(text="Total time elapsed: "+str(self.timeT))

        if(self.pauseCondition == False):
            self.auxProcess.te = self.auxProcess.te + 1
        
        count = 0
        for i in self.blockedArr: #iterate in blocked list
            self.blockedLblArr[count].config(text="ID: " + str(i.pid) +"\n" + "TTB: " + str(i.ttb)) #Update values
            self.blockedLblArr[count].grid(row=0,column=count, padx=15, pady=15) #pack them (show them in the GUI)
            count += 1


        if(self.pauseCondition == False):
            self.timeT = self.timeT + 1
             
            for i in self.readyArr:
                 if(i.te == 0):
                     i.resT = i.resT + 1
            
            for i in self.blockedArr: #update time to every process in blocked list
                i.ttb = i.ttb + 1

        if(self.auxProcess.te == self.auxProcess.met + 1):
            self.lbl1.config(text="ID: ")
            self.lbl2.config(text="OP: ")
            self.lbl3.config(text="MET: ")
            self.lbl4.config(text="TE: ")
            self.lbl5.config(text="TR: ")
            self.showPCB()
            return

        self.processingWindow.bind("<Key>", self.keyHandler) #keypress detection

        self.processingWindow.after(1000, self.updateProcessing)

# Execute program
if __name__ == "__main__":

    OperativeSystemApp()