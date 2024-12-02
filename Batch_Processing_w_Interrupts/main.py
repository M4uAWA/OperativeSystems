import random
import tkinter as tk
from tkinter import ttk
from process import Process
from batch import Batch
from queue import Queue
from ctypes import windll  # IMPROVE RESOLUTION

windll.shcore.SetProcessDpiAwareness(1)

class OperativeSystemApp:
    def __init__(self):
        # initial config
        self.bS = 5  # batch size
        self.entVar = None
        
        # processing variables
        self.batchQueue = Queue()
        self.auxBatch = Batch(self.bS)
        self.tNew = None
        self.operators = "+-*/%"
        self.processArr = []
        self.doneArr = []
        self.timeT = 0
        self.timeChange = 0
        self.flag = False
        self.batchCounter = 0
        self.pauseCondition = False
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

    def submitC(self):
        self.entVar = int(self.txtVar.get())
        self.window.destroy()
        self.tNew = self.entVar

    def processCapture(self):
        i = 0
        
        while (self.tNew != 0):
            self.auxProcess = Process()
            name = "Process" + str(i+1)
            meOma0 = int(random.randrange(1,2))
            self.auxProcess.name = name
            self.auxProcess.pid = i+1
            self.auxProcess.x = int(random.randrange(-99,99))
            self.auxProcess.operation = random.choice(self.operators)
            
            if(self.auxProcess.operation == "/" or self.auxProcess.operation == "%"):
                if(meOma0 == 1):
                    self.auxProcess.y = int(random.randrange(1,99))
                else:
                    self.auxProcess.y = int(random.randrange(-99,-1))
            else:
                self.auxProcess.y = int(random.randrange(-99,99))
            self.auxProcess.met = int(random.randrange(5,25))
            
            if(self.auxProcess.operation == "/"):
                self.auxProcess.result = round(self.auxProcess.x / self.auxProcess.y,2)
                self.auxProcess.fullOpe = str(self.auxProcess.x) + self.auxProcess.operation + str(self.auxProcess.y)

            elif(self.auxProcess.operation == "%"):
                self.auxProcess.result = round(self.auxProcess.x % self.auxProcess.y,2)
                self.auxProcess.fullOpe = str(self.auxProcess.x) + self.auxProcess.operation + str(self.auxProcess.y)

            elif(self.auxProcess.operation == "+"):
                self.auxProcess.result = round(self.auxProcess.x + self.auxProcess.y,2)
                self.auxProcess.fullOpe = str(self.auxProcess.x) + self.auxProcess.operation + str(self.auxProcess.y)

            elif(self.auxProcess.operation == "-"):
                self.auxProcess.result = round(self.auxProcess.x - self.auxProcess.y,2)
                self.auxProcess.fullOpe = str(self.auxProcess.x) + self.auxProcess.operation + str(self.auxProcess.y)

            elif(self.auxProcess.operation == "*"):
                self.auxProcess.result = round(self.auxProcess.x * self.auxProcess.y,2)
                self.auxProcess.fullOpe = str(self.auxProcess.x) + self.auxProcess.operation + str(self.auxProcess.y)

            #Process enqueue

            if(self.auxBatch.processQueue.full()):     #When reaching batch size, enqueue batch
                self.batchQueue.put(self.auxBatch)
                self.auxBatch = Batch(self.bS)

            self.auxBatch.processQueue.put(self.auxProcess)

            i += 1
            self.tNew -= 1 #Decrement remaining processes

        if(not self.auxBatch.processQueue.empty()): #Case - Queuing an incomplete batch
            self.batchQueue.put(self.auxBatch)

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

        self.lbl = self.labelFormat(self.loadingWindow,"\n\n\n\n\nGenerating operations...\n")
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
        self.processArr = []
        self.doneArr = [] #array to store finished processes (it is initialized here because they are permanent)

        self.processingWindow.columnconfigure(0, weight=1)
        self.processingWindow.columnconfigure(1, weight=1)
        self.processingWindow.columnconfigure(2, weight=1)

        self.timeT = 0
        self.flag = False
        self.batchCounter = 0
        self.pauseCondition = False


        #left panel


        self.lbl01 = self.labelFormat(self.processingWindow,"\nNumber of Batches remaining: " + str(self.batchQueue.qsize()))
        self.lbl01.grid(row=0, column=2)

        self.lf0 = tk.LabelFrame(self.processingWindow, text="Curret Batch", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        self.lf0.grid(row=1, column=0, padx=20, sticky=tk.NSEW)

        self.lbl02 = self.labelFormat(self.lf0, "Name   MET    TE")
        self.lbl02.pack()

        self.lbl00 = tk.Label(self.lf0, text="",bg="#000000",justify=tk.CENTER, font=('Century Gothic',12), foreground='#d7c7ff')
        self.lbl00.pack() #pending processes


        #middle panel


        self.lf1 = tk.LabelFrame(self.processingWindow, text="Processing", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
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
        self.lbl6 = tk.Label(self.lf1, text="",bg="#000000", font=('Century Gothic',12), foreground='#d7c7ff')
        self.lbl6.pack(anchor="w")


        #right panel


        self.lf2 = tk.LabelFrame(self.processingWindow, text="Done", padx=10, pady=10, font=('Century Gothic',12), bg="#000000", foreground='#d7c7ff')
        self.lf2.grid(row=1, column=2, padx=20, sticky=tk.NSEW)

        self.lbl7 = self.labelFormat(self.lf2,"ID      OP    ANS")
        self.lbl7.pack()

        self.lbl9 = tk.Label(self.lf2, text="",bg="#000000",justify=tk.CENTER, font=('Century Gothic',12), foreground='#d7c7ff')
        self.lbl9.pack() #done

        self.lbl10 = tk.Label(self.processingWindow, text="Total time elapsed: 0",bg="#000000",justify=tk.CENTER, font=('Century Gothic',12), foreground='#d7c7ff')#done
        self.lbl10.grid(row=2, column=2, padx=20)

        self.updateProcessing()

        self.processingWindow.mainloop()

    def keyHandler(self, key):
        if self.pauseCondition == False:
            if int(key.keycode) == 69:  # ERROR - E
                self.auxProcess.result = "ERROR"
                self.auxProcess.tE = self.auxProcess.met  # Trigger new process assignment
                
            elif int(key.keycode) == 73:  # INTERRUPTION - I
                if(self.timeChange != self.timeT): #Check if interruption was pressed twice in the same second (prevents decrementing te of a process in readyarr)
                    self.auxProcess.tE = self.auxProcess.tE - 1
                self.processArr.append(self.auxProcess) 
                self.auxProcess = self.processArr.pop(0) #assign process currently being processed and pop previous process from current batch process array
                
            elif int(key.keycode) == 80:  # PAUSE - P
                self.lf1.config(text="Paused")
                self.pauseCondition = True
                if(self.timeChange != self.timeT):
                    self.timeT -= 1
                    self.auxProcess.tE -= 1
                
        if int(key.keycode) == 67:  # CONTINUE - C
            self.lf1.config(text="Processing")
            self.pauseCondition = False
            if(self.timeChange != self.timeT):
                self.timeT += 1
                self.auxProcess.tE += 1
            
        self.timeChange = self.timeT #sets the time at which the interruption was made

    def updateProcessing(self):

        if(self.auxProcess.tE == self.auxProcess.met):
            if(not self.auxProcess.pid == None):
                self.doneArr.append(self.auxProcess)

            if(len(self.processArr) > 0):
                self.auxProcess = self.processArr[0] #assign process currently being processed
                self.processArr.pop(0) #pop it from current batch processes array

            else:
                self.flag = False

        if(len(self.processArr) == 0 and self.flag == False): #get new batch and fill processArr with current batch processes
            if (not self.batchQueue.empty()):
                currentBatch = self.batchQueue.get()

                self.batchCounter += 1
                batchNum = Process()
                batchNum.pid = ""
                batchNum.fullOpe = "- Batch number: " + str(self.batchCounter) +" -"
                batchNum.result = ""

                self.doneArr.append(batchNum)

                for i in range(currentBatch.processQueue.qsize()):
                    self.processArr.append(currentBatch.processQueue.get())

                self.auxProcess = self.processArr[0] #assign process currently being processed
                self.processArr.pop(0) #pop it from current batch processes array
                self.flag = True

        self.lbl01.config(text="\nNumber of pending batches: " + str(self.batchQueue.qsize()))

        self.processStr = ""
        for i in self.processArr:
            self.processStr = self.processStr + str(i.name)+ "    " +str(i.met) + "    " +str(i.tE) +"\n"
        self.lbl00.config(text=self.processStr)

        self.lbl1.config(text="ID: " + str(self.auxProcess.pid))
        self.lbl2.config(text="OP: " + str(self.auxProcess.fullOpe))
        self.lbl3.config(text="MET: " + str(self.auxProcess.met))
        self.lbl4.config(text="NAME: " + str(self.auxProcess.name))
        self.lbl5.config(text="TE: " + str(self.auxProcess.tE))
        self.lbl6.config(text="TR: " + str(self.auxProcess.met - self.auxProcess.tE))

        doneStr =""
        for i in self.doneArr:
          doneStr = doneStr + str(i.pid) + "    " + str(i.fullOpe) + "   " + str(i.result) + "\n"
        self.lbl9.config(text=doneStr)

        self.lbl10.config(text="Total time elapsed: "+str(self.timeT))

        if(self.pauseCondition == False):
            self.auxProcess.tE = self.auxProcess.tE + 1

        if(self.pauseCondition == False):
            self.timeT = self.timeT + 1

        if(self.auxProcess.tE == self.auxProcess.met + 1):
            self.lbl1.config(text="ID: ")
            self.lbl2.config(text="OP: ")
            self.lbl3.config(text="MET: ")
            self.lbl4.config(text="NAME: ")
            self.lbl5.config(text="TE: ")
            self.lbl6.config(text="TR: ")
            return

        self.processingWindow.bind("<Key>", self.keyHandler) #keypress detection

        self.processingWindow.after(1000, self.updateProcessing)

# Execute program
if __name__ == "__main__":
    
    OperativeSystemApp()