import Tkinter as tk
#~ import socket
#~ import select
import os
import sys
import threading
import subprocess
import atexit
import signal
#~ import struct
#~ import binascii
#~ import time

myThread = None

class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        #~ self.sequenceList = [
            #~ "collide_1.txt",
            #~ "fire.txt",
            #~ "halloween_1.txt",
            #~ "july4th_1.txt",
            #~ "july4th_2.txt",
            #~ "max_brightness.txt",
            #~ "off.txt",
            #~ "rainbow_slow.txt",
            #~ "stpats_1.txt",
            #~ "test_sequence_1.txt",
            #~ "test_sequence_2.txt",
            #~ "test_sequence_3.txt",
            #~ "test_sequence_4.txt",
            #~ "test_sequence_5.txt",
            #~ "test.txt",
            #~ "xmas_1.txt",
            #~ ]
            
        self.sequenceList = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.txt'):
                    self.sequenceList.append(file)
                    print file
        self.sequenceList.sort()
            
        self.maxColumns = 5
        self.maxRows = 7

        self.createWidgets()
        self.currentThreadIndex = None




    def createWidgets(self):

        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1, minsize=450)
        top.columnconfigure(0, weight=1, minsize=750)

        # create labelframe box
        self.labelFrame = tk.LabelFrame(top, text="Available" )
        self.labelFrame.grid(column=0, row=0, sticky=tk.N+tk.S+tk.E+tk.W, padx=2, pady=2)
        self.labelFrame.rowconfigure(0, weight=1, minsize=10)
        self.labelFrame.columnconfigure(0, weight=1, minsize=10)

        # create button list
        self.buttonList = []
        row = 0
        col = 0
        for rowIndex in range(self.maxRows):
            for colIndex in range(self.maxColumns):
            
                parent = self.labelFrame
                seqIndex = rowIndex*self.maxColumns + colIndex
                if len(self.sequenceList) > seqIndex:
                    myButton = tk.Button(parent, text=self.sequenceList[seqIndex],
                           command=lambda seqIndex=seqIndex: self.startButtonHandler(seqIndex) )
                    myButton.grid(column=colIndex, row=rowIndex, sticky=tk.N+tk.S+tk.E+tk.W, padx=2, pady=2)
                    myButton.rowconfigure(rowIndex, weight=1, minsize=10)
                    myButton.columnconfigure(colIndex, weight=1, minsize=10)
                    myButton.configure(bg = "#d9d9d9")
                    myButton.configure(activebackground = "#ececec")
                    parent.rowconfigure(rowIndex, weight=1)
                    parent.columnconfigure(colIndex, weight=1, minsize=30)
                    self.buttonList.append(myButton)

    def startButtonHandler(self,seqIndex):
        print("Start sequence %s" % (self.sequenceList[seqIndex]))

        command = ''

        command = command + 'sudo ../test -f %s' % (self.sequenceList[seqIndex])

        print("command=%s" % command)
        
        
        self.run_command(command, seqIndex)

    def run_command(self, command, seqIndex):
        global myThread


        if myThread != None:
            print("Stop Thread %s" % (self.sequenceList[seqIndex]))
            myThread.send_signal(signal.SIGINT)  
            #~ killCommandProc = subprocess.Popen("\"sudo kill $(ps -ef | grep sudo | grep test| grep -v /bin/sh | awk '{print($2)}')\"", stderr=subprocess.PIPE, shell=True)
            #~ killCommandProc = subprocess.Popen("echo $(ps -ef | grep sudo | grep test| grep -v /bin/sh )", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            #~ killCommandProc.wait()  # will block here.
            #~ stdoutdata, stderrdata = killCommandProc.communicate()  # will block here.
            #~ print stdoutdata , stderrdata
          
        else:
            self.buttonList[seqIndex].configure(bg = "red")
            self.buttonList[seqIndex].configure(activebackground = "red")
            
            # do thread stuff
            print("Starting Thread %s" % (self.sequenceList[seqIndex]))
            t = threading.Thread(target=self.command_thread, name="Sequence Thread", args=(command, seqIndex))
            t.start()




    def command_thread(self, command, seqIndex):
        global myThread
        print "do stuff"

        # vrlinux = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        myThread = subprocess.Popen("exec "+command, stderr=subprocess.PIPE, shell=True)
        self.currentThreadIndex = seqIndex

        myThread.wait()  # will block here.
        stdoutdata, stderrdata = myThread.communicate()  # will block here.
        print stderrdata


        print("Thread ending")
        myThread = None

    def periodicEventHandler(self):
        self.after(100,self.periodicEventHandler); # poll every 100msec

        global myThread
        if (myThread == None) and (self.currentThreadIndex != None):
            self.buttonList[self.currentThreadIndex].configure(bg = "#d9d9d9")
            self.buttonList[self.currentThreadIndex].configure(activebackground = "#ececec")
            self.currentThreadIndex = None



def cleanup():
    global myThread
    # kill the process in case its still around

    if myThread != None:
        myThread.send_signal(signal.SIGINT)

        print("killed stray thread")
    #~ my_threads = None


def main():
    app = Application()
    app.master.title('sequence Launcher')
    #~ app.getSettings()

    atexit.register(cleanup) # use atexit to make sure cleanup happens even in a crash

    app.after(500,app.periodicEventHandler)
    try:
        app.mainloop()
    finally:
        print("doing finally")
        cleanup()



if __name__ == "__main__":
    main()
