# coding = utf-8
import subprocess
import os
import tempfile
import time
from subprocess import Popen, PIPE
import psutil

class watchdogProcessManager:
    def __init__(self,commands):
        self.processIndex={}
        self.f=tempfile.TemporaryFile()
        self.commands=commands
    def runProcess(self,index):
        command=self.commands[index]
        p = subprocess.Popen(
            [command],
            stdout=self.f,
            stderr=subprocess.STDOUT,
            stdin=PIPE,
            shell=True,
            bufsize=0
        )
        self.processIndex[index]=p
        print("running at pid("+str(p.pid)+"): "+command)
    def rerunProcessWhenDown(self,index):
        print("process index: "+str(self.processIndex[index].pid)+" Poll: "+str(self.processIndex[index].poll()))
        if not self.processIndex[index].poll() is None:
            print("the process with the following index is death: "+str(index))
            self.runProcess(index)
    def executeWatchDog(self):
        for i in range(len(self.commands)):
            self.runProcess(i)
        time.sleep(3)
        while True:
            print("watching...")
            for i in range(len(self.commands)):
                self.rerunProcessWhenDown(i)
            time.sleep(3)

commandsFile=open("commands.txt", "r")
lines=commandsFile.readlines()
print(lines)
commands=[]
for i in lines:
    commands.append(i[:len(i)-1])
watchdog=watchdogProcessManager(commands)
watchdog.executeWatchDog()
