#~ import Tkinter as tk
import socket
import select
import os
import sys
import threading
import subprocess
import atexit
import signal
#~ import struct
#~ import binascii
import time

myThread = None

class Application():

    def __init__(self):

        self.sequenceList = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.txt'):
                    self.sequenceList.append(file)
                    print "<%s>" % file
             
        self.setupNetworkStuff()

    def setupNetworkStuff(self):
        self.port = 59410
        self.remoteAddress = "127.0.0.1"

        self.socket = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM) # UDP
        self.socket.setblocking(False)

        self.socket.bind(('0.0.0.0', self.port))


    #~ def createWidgets(self):
#~ 
        #~ top=self.winfo_toplevel()
        #~ top.rowconfigure(0, weight=1, minsize=450)
        #~ top.columnconfigure(0, weight=1, minsize=750)
#~ 
        #~ # create labelframe box
        #~ self.labelFrame = tk.LabelFrame(top, text="Available" )
        #~ self.labelFrame.grid(column=0, row=0, sticky=tk.N+tk.S+tk.E+tk.W, padx=2, pady=2)
        #~ self.labelFrame.rowconfigure(0, weight=1, minsize=10)
        #~ self.labelFrame.columnconfigure(0, weight=1, minsize=10)
#~ 
        #~ # create button list
        #~ self.buttonList = []
        #~ row = 0
        #~ col = 0
        #~ for rowIndex in range(self.maxRows):
            #~ for colIndex in range(self.maxColumns):
            #~ 
                #~ parent = self.labelFrame
                #~ seqIndex = rowIndex*self.maxColumns + colIndex
                #~ if len(self.sequenceList) > seqIndex:
                    #~ myButton = tk.Button(parent, text=self.sequenceList[seqIndex],
                           #~ command=lambda seqIndex=seqIndex: self.startButtonHandler(seqIndex) )
                    #~ myButton.grid(column=colIndex, row=rowIndex, sticky=tk.N+tk.S+tk.E+tk.W, padx=2, pady=2)
                    #~ myButton.rowconfigure(rowIndex, weight=1, minsize=10)
                    #~ myButton.columnconfigure(colIndex, weight=1, minsize=10)
                    #~ myButton.configure(bg = "#d9d9d9")
                    #~ myButton.configure(activebackground = "#ececec")
                    #~ parent.rowconfigure(rowIndex, weight=1)
                    #~ parent.columnconfigure(colIndex, weight=1, minsize=30)
                    #~ self.buttonList.append(myButton)

    #~ def startButtonHandler(self,seqIndex):
        #~ print("Start sequence %s" % (self.sequenceList[seqIndex]))
#~ 
        #~ command = ''
#~ 
        #~ command = command + 'sudo ../test -f %s' % (self.sequenceList[seqIndex])
#~ 
        #~ print("command=%s" % command)
        #~ 
        #~ 
        #~ self.run_command(command, seqIndex)

    def run_command(self, command):
        global myThread


        if myThread != None:
            print("Stop Thread")
            myThread.send_signal(signal.SIGINT)
            time.sleep(0.5)

        # do thread stuff
        print("Starting Thread")
        t = threading.Thread(target=self.command_thread, name="Sequence Thread", args=(command, 1))
        t.start()




    def command_thread(self, command, one):
        global myThread
        print "do stuff"

        # vrlinux = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        myThread = subprocess.Popen("exec "+command, stderr=subprocess.PIPE, shell=True)

        myThread.wait()  # will block here.
        stdoutdata, stderrdata = myThread.communicate()  # will block here.
        print stderrdata


        print("Thread ending")
        myThread = None

    #~ def periodicEventHandler(self):
        #~ self.after(100,self.periodicEventHandler); # poll every 100msec
#~ 
        #~ global myThread
        #~ if (myThread == None) and (self.currentThreadIndex != None):
            #~ self.buttonList[self.currentThreadIndex].configure(bg = "#d9d9d9")
            #~ self.buttonList[self.currentThreadIndex].configure(activebackground = "#ececec")
            #~ self.currentThreadIndex = None

    def checkForCommand(self):
        queue_empty = False
        returnVal = None
        while queue_empty == False:
            ready_to_read, ready_to_write, in_error = select.select([self.socket], [], [], 0.001) # wait 1 msec

            if len(ready_to_read) == 0:
                queue_empty = True
            else:
                data, address = ready_to_read[0].recvfrom(4096)

                data = data.rstrip()
                print('received <%s>' % data)
                if data in self.sequenceList:
                    print('command is valid %s' % data)
                    returnVal = data
                    
        return returnVal

    def runFile(self, fileToRun):
        if fileToRun != None:
            command = ''
            command = command + 'sudo ../test -f %s' % (fileToRun)
            print("command=%s" % command)

            self.run_command(command)

    def run(self):
        while True:
            fileToRun = self.checkForCommand()
            self.runFile(fileToRun)
            time.sleep(0.1)

def cleanup():
    global myThread
    # kill the process in case its still around

    if myThread != None:
        myThread.send_signal(signal.SIGINT)

        print("killed stray thread")
    #~ my_threads = None


def main():
    app = Application()
    #~ app.master.title('sequence Launcher')
    #~ app.getSettings()

    atexit.register(cleanup) # use atexit to make sure cleanup happens even in a crash

    #~ app.after(500,app.periodicEventHandler)
    try:
        app.run()
    finally:
        print("doing finally")
        cleanup()



if __name__ == "__main__":
    main()
