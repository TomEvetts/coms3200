#!/usr/bin/python3
# Author Tom Evetts 
# Control UI for EDAQs network to interface with i2c driver

import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Text, Tk
import os
import subprocess
from subprocess import Popen, PIPE
import sys
import time
import select
from threading import Thread
import threading

from bluetooth import *
import sys

#includes for the text file
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import re
import time

import fileread as fr

if sys.version < '3':
    input = raw_input

global addr
addr = None

global bluetoothActive
bluetoothActive = 0
sock=BluetoothSocket( RFCOMM )

#     opens the serial port for the bluetooth device

#    returns true if it is open, use this to check

linebuffer=[] #buffer used to store and print serial data
#x = subprocess.Popen([r"D:\thesis\driver/driver.exe"], stdout=PIPE, stdin=PIPE, stderr=PIPE)  #subprocess that is the c program that runs the i2c
#x = subprocess.Popen([r"D:\thesis\driver/dr.exe"], stdout=PIPE, stdin=PIPE, stderr=PIPE)  #subprocess that is the c program that runs the i2c
x = subprocess.Popen([r"D:\thesis\driver\Test_throughputerrors/driverslow.exe"], stdout=PIPE, stdin=PIPE, stderr=PIPE)


#find and replace a section in a file
def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                
                if (line.find(pattern) != -1):
                    line, sep, tail = line.partition('=')
                    line+subst
                    line + '\n'
                    
                new_file.write(line)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


    
#this function is used to detect the incoming serial fron the program
def reader(f,buffer, t, self):
   global bluetoothActive
   while True:
     if bluetoothActive :
        line = sock.recv(1024)
     else :
        line=f.readline()
     if line:
        buffer.append(line)
        ##perform string processing in here before popping
        #if linebuffer[0].find("ADC"):
        str1 = ""
        str1 = linebuffer[0];
        print( str1 )
            
        if (str1.find(b"ADC") != -1):
            print( "got it " )
        if (str1.find(b"addresses connected") != -1):
            ######clear it before writing
            self.entry_connected.delete(0, 'end')
            self.entry_connected.insert(tkinter.END, linebuffer[0][29:])
        if (str1.find(b"State!: 37") != -1):
            ######clear it before writing
            self.entry_mcpstat.delete(0, 'end')
            self.entry_mcpstat.insert(tkinter.END, "NACK, check addr & connection health")
        if (str1.find(b"State!: 37") != -1):
            ######clear it before writing
            self.entry_mcpstat.delete(0, 'end')
            self.entry_mcpstat.insert(tkinter.END, "STOP, check system health resend command")
        if (str1.find(b"MCP2221 unresponsive 600") != -1):
            ######clear it before writing
            self.entry_mcpstat.delete(0, 'end')
            self.entry_mcpstat.insert(tkinter.END, "Connection lost, restart program")
        if (str1.find(b"net_state") != -1): 
            if (str1.find(b"1") != -1):
                self.entry_netstat.delete(0, 'end')
                self.entry_netstat.insert(tkinter.END, b"Busy")
            else:
                self.entry_netstat.delete(0, 'end')
                self.entry_netstat.insert(tkinter.END, b"Ready")
        if (str1.find(b"BT CSV") != -1):
            print( "receving CSV file\n" )
            getFile(sock, "file.csv", 1024)
        
        t.insert(tkinter.END, linebuffer.pop())
     else:
        print('program closed in background')
        break

def getFile(self, gotPath, packageSize):
    """
    Collects arriving packets
    """
    if (packageSize == None):
        packageSize = 102400
    name = self.recv(15)
    #name = recv_timeout(self)
    print( "Name = " )
    print( name )
    print( "\n\n\n" )
    f = open(name, 'w+')
    packet = 1

    data = ''
    n = 100000
    while 1:
        packet = sock.recv(1024)
        if (packet.find(b"EOF") != -1):
            f.write(packet.decode('utf-8'))
            break
        data += packet.decode('utf-8')
        f.write(packet.decode('utf-8'))
        
        
    
    
    self.isFileGot= True
    f.close()
    print ("File Recieved")

def recv_timeout(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)
     
    #total data partwise in an array
    total_data=[];
    data='';
     
    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
         
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
         
        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
     
    #join all parts to make final string
    return ''.join(total_data.decode('utf-8'))

def check_netstat_glob():
        global bluetoothActive
        if bluetoothActive == 0:
           x.stdin.write(bytes("52 h \n", "ascii"))
           x.stdin.flush()
        else :
           sock.send(bytes("52 h \n", "ascii"))


class popupWindow(object):
    def __init__(self,master):
        top =self.top = tkinter.Toplevel()
        top.wm_title("Set Values")

        l0 = tkinter.Label(top, text="Set PLL")
        l0.grid(row=0, column=0)

        self.entry_Pll = ttk.Entry(top, width = 24, font = ('Arial', 10))
        self.entry_Pll.grid(row = 0, column = 1, padx = 5, pady = 5)

        l = tkinter.Label(top, text="Set Storage")
        l.grid(row=1, column=0)

        b = ttk.Button(top, text="Send", command=self.cleanup)
        b.grid(row=11, column=0)
        #this is to be annother pop up box that explains every input and how to use
        b1 = ttk.Button(top, text="Help", command=self.cleanup)
        b1.grid(row=11, column=1)
        self.entry_Storage = ttk.Entry(top, width = 24, font = ('Arial', 10))
        self.entry_Storage.grid(row = 1, column = 1, padx = 5, pady = 5)

        l1 = tkinter.Label(top, text="Set Number of signals")
        l1.grid(row=2, column=0)

        self.entry_Signals = ttk.Entry(top, width = 24, font = ('Arial', 10))
        self.entry_Signals.grid(row = 2, column = 1, padx = 5, pady = 5)
##       set total_samples <value>
        l2 = tkinter.Label(top, text="Set total Samples")
        l2.grid(row=3, column=0)


        self.entry_Samples = ttk.Entry(top, width = 24, font = ('Arial', 10))
        self.entry_Samples.grid(row = 3, column = 1, padx = 5, pady = 5)
##       set sample_period_us <value>
        l3 = tkinter.Label(top, text="Set sample period")
        l3.grid(row=4, column=0)

        self.entry_Period = ttk.Entry(top, width = 24, font = ('Arial', 10))
        self.entry_Period.grid(row = 4, column = 1, padx = 5, pady = 5)
##       set post_trigger_samples <value>
        l4 = tkinter.Label(top, text="Set Post Trigger Samples")
        l4.grid(row=5, column=0)

        self.entry_Post = ttk.Entry(top, width = 24, font = ('Arial', 10))
        self.entry_Post.grid(row = 5, column = 1, padx = 5, pady = 5)
##       set trigger_source <int|ext>
        l5 = tkinter.Label(top, text="Trigger Source")
        l5.grid(row=6, column=0)

        self.entry_Trigger_source = ttk.Entry(top, width = 24, font = ('Arial', 10))
        self.entry_Trigger_source.grid(row = 6, column = 1, padx = 5, pady = 5)
##       set trigger_signal <value>
        l6 = tkinter.Label(top, text="Set trigger signal")
        l6.grid(row=7, column=0)

        self.entry_Trigger_signal = ttk.Entry(top, width = 24, font = ('Arial', 10))
        self.entry_Trigger_signal.grid(row = 7, column = 1, padx = 5, pady = 5)
##       set trigger_level <value>
        l7 = tkinter.Label(top, text="Set Trigger Level")
        l7.grid(row=8, column=0)

        self.entry_Trigger_level = ttk.Entry(top, width = 24, font = ('Arial', 10))
        self.entry_Trigger_level.grid(row = 8, column = 1, padx = 5, pady = 5)
##       set trigger_slope +|-
        l8 = tkinter.Label(top, text="Set Trigger Slope")
        l8.grid(row=9, column=0)

        self.entry_Trigger = ttk.Entry(top, width = 24, font = ('Arial', 10))
        self.entry_Trigger.grid(row = 9, column = 1, padx = 5, pady = 5)

        l9 = tkinter.Label(top, text="Addresses to send to")
        l9.grid(row=10, column=0)

        self.entry_Addrs = ttk.Entry(top, width = 24, font = ('Arial', 10))
        self.entry_Addrs.grid(row = 10, column = 1, padx = 5, pady = 5)

    def cleanup(self):
        #need to loop through all addresses put in the address box, or All, if all is put in this box

        global bluetoothActive


        string1 = self.entry_Addrs.get()
        mylist = []
        mylist = string1.split(' ')
        print( mylist )
        for i in range(mylist.__len__()):
            #print( mylist[i] )
            if mylist[i] == '':
                print( "danger danger" )
            else:# we can send it add extra checks for non intiger variables

                if self.entry_Pll.get():
                   print( "got it")
                   if bluetoothActive == 0:
                       #FYC speed
                       x.stdin.write(bytes(mylist[i], "ascii"))
                       x.stdin.write(bytes(" w 1 ", "ascii"))## is only 4 for testing
                       x.stdin.write(bytes(self.entry_Pll.get(), "ascii"))
                       x.stdin.write(bytes("\n", "ascii"))
                       x.stdin.flush()
                       time.sleep(0.25)
                   else :

                       sock.send(bytes(mylist[i], "ascii"))
                       sock.send(bytes(" w 1 ", "ascii"))## is only 4 for testing
                       sock.send(bytes(self.entry_Pll.get(), "ascii"))
                       sock.send(bytes("\n", "ascii"))
                       time.sleep(0.25)


                if self.entry_Storage.get():
                   print( "got it1")
                   if bluetoothActive == 0:
                       #Storage int or ext 00 or FF
                       x.stdin.write(bytes(mylist[i], "ascii"))
                       x.stdin.write(bytes(" w 2 ", "ascii"))## is only 4 for testing
                       x.stdin.write(bytes(self.entry_Storage.get(), "ascii"))
                       x.stdin.write(bytes("\n", "ascii"))
                       x.stdin.flush()
                       time.sleep(0.25)
                   else :
                       sock.send(bytes(mylist[i], "ascii"))
                       sock.send(bytes(" w 2 ", "ascii"))## is only 4 for testing
                       sock.send(bytes(self.entry_Storage.get(), "ascii"))
                       sock.send(bytes("\n", "ascii"))
                       time.sleep(0.25)


                if self.entry_Signals.get():
                   print( "got it2")
                   if bluetoothActive == 0:
                       #number of signals
                       x.stdin.write(bytes(mylist[i], "ascii"))
                       x.stdin.write(bytes(" w 5 ", "ascii"))## is only 4 for testing
                       x.stdin.write(bytes(self.entry_Signals.get(), "ascii"))
                       x.stdin.write(bytes("\n", "ascii"))
                       x.stdin.flush()
                       time.sleep(0.25)
                   else :
                       sock.send(bytes(mylist[i], "ascii"))
                       sock.send(bytes(" w 5 ", "ascii"))## is only 4 for testing
                       sock.send(bytes(self.entry_Signals.get(), "ascii"))
                       sock.send(bytes("\n", "ascii"))
                       time.sleep(0.25)


                if self.entry_Samples.get():
                   print( "got it3")
                   if bluetoothActive == 0:
                       #total samples
                       x.stdin.write(bytes(mylist[i], "ascii"))
                       x.stdin.write(bytes(" w 6 ", "ascii"))## is only 4 for testing
                       samples_i = int(self.entry_Samples.get())
                       samples_i_low = samples_i & 0xFF
                       samples_i_high = samples_i >> 8
                       samples_i_low = format(samples_i_low, 'x')
                       samples_i_high = format(samples_i_high, 'x')
                       x.stdin.write(bytes(samples_i_low, "ascii"))
                       x.stdin.write(bytes(" ", "ascii"))
                       x.stdin.write(bytes(samples_i_high, "ascii"))
                       x.stdin.write(bytes("\n", "ascii"))
                       x.stdin.flush()
                       time.sleep(0.25)
                   else :
                       sock.send(bytes(mylist[i], "ascii"))
                       sock.send(bytes(" w 6 ", "ascii"))## is only 4 for testing
                       samples_i = int(self.entry_Samples.get())
                       samples_i_low = samples_i & 0xFF
                       samples_i_high = samples_i >> 8
                       samples_i_low = format(samples_i_low, 'x')
                       samples_i_high = format(samples_i_high, 'x')
                       sock.send(bytes(samples_i_low, "ascii"))
                       sock.send(bytes(" ", "ascii"))
                       sock.send(bytes(samples_i_high, "ascii"))
                       sock.send(bytes("\n", "ascii"))
                       time.sleep(0.25)


                if self.entry_Period.get():
                   print( "got it4")
                   if bluetoothActive == 0:
                       #sampling period
                       x.stdin.write(bytes(mylist[i], "ascii"))
                       x.stdin.write(bytes(" w 7 ", "ascii"))## is only 4 for testing
                       samples_i = int(self.entry_Period.get())
                       samples_i_low = samples_i & 0xFF
                       samples_i_high = samples_i >> 8
                       samples_i_low = format(samples_i_low, 'x')
                       samples_i_high = format(samples_i_high, 'x')
                       x.stdin.write(bytes(samples_i_low, "ascii"))
                       x.stdin.write(bytes(" ", "ascii"))
                       x.stdin.write(bytes(samples_i_high, "ascii"))
                       x.stdin.write(bytes("\n", "ascii"))
                       x.stdin.flush()
                       time.sleep(0.25)
                   else :
                       sock.send(bytes(mylist[i], "ascii"))
                       sock.send(bytes(" w 7 ", "ascii"))## is only 4 for testing
                       samples_i = int(self.entry_Period.get())
                       samples_i_low = samples_i & 0xFF
                       samples_i_high = samples_i >> 8
                       samples_i_low = format(samples_i_low, 'x')
                       samples_i_high = format(samples_i_high, 'x')
                       sock.send(bytes(samples_i_low, "ascii"))
                       sock.send(bytes(" ", "ascii"))
                       sock.send(bytes(samples_i_high, "ascii"))
                       sock.send(bytes("\n", "ascii"))
                       time.sleep(0.25)


                if self.entry_Post.get():
                   print( "got it5")
                   if bluetoothActive == 0:
                       #post trigger samples
                       x.stdin.write(bytes(mylist[i], "ascii"))
                       x.stdin.write(bytes(" w 8 ", "ascii"))## is only 4 for testing
                       samples_i = int(self.entry_Post.get())
                       samples_i_low = samples_i & 0xFF
                       samples_i_high = samples_i >> 8
                       samples_i_low = format(samples_i_low, 'x')
                       samples_i_high = format(samples_i_high, 'x')
                       x.stdin.write(bytes(samples_i_low, "ascii"))
                       x.stdin.write(bytes(" ", "ascii"))
                       x.stdin.write(bytes(samples_i_high, "ascii"))
                       x.stdin.write(bytes("\n", "ascii"))
                       x.stdin.flush()
                       time.sleep(0.25)
                   else :
                       sock.send(bytes(mylist[i], "ascii"))
                       sock.send(bytes(" w 8 ", "ascii"))## is only 4 for testing
                       samples_i = int(self.entry_Post.get())
                       samples_i_low = samples_i & 0xFF
                       samples_i_high = samples_i >> 8
                       samples_i_low = format(samples_i_low, 'x')
                       samples_i_high = format(samples_i_high, 'x')
                       sock.send(bytes(samples_i_low, "ascii"))
                       sock.send(bytes(" ", "ascii"))
                       sock.send(bytes(samples_i_high, "ascii"))
                       sock.send(bytes("\n", "ascii"))
                       time.sleep(0.25)


                if self.entry_Trigger_source.get():
                   print( "got it6")
                   if bluetoothActive == 0:
                       #trigger source int or ext
                       x.stdin.write(bytes(mylist[i], "ascii"))
                       x.stdin.write(bytes(" w 9 ", "ascii"))## is only 4 for testing
                       x.stdin.write(bytes(self.entry_Trigger_source.get(), "ascii"))
                       x.stdin.write(bytes("\n", "ascii"))
                       x.stdin.flush()
                       time.sleep(0.25)
                   else :
                       sock.send(bytes(mylist[i], "ascii"))
                       sock.send(bytes(" w 9 ", "ascii"))## is only 4 for testing
                       sock.send(bytes(self.entry_Trigger_source.get(), "ascii"))
                       sock.send(bytes("\n", "ascii"))
                       time.sleep(0.25)


                if self.entry_Trigger_signal.get():
                   print( "got it7")
                   if bluetoothActive == 0:
                       #trigger signal select
                       x.stdin.write(bytes(mylist[i], "ascii"))
                       x.stdin.write(bytes(" w A ", "ascii"))## is only 4 for testing
                       x.stdin.write(bytes(self.entry_Trigger_signal.get(), "ascii"))
                       x.stdin.write(bytes("\n", "ascii"))
                       x.stdin.flush()
                       time.sleep(0.25)
                   else :
                       sock.send(bytes(mylist[i], "ascii"))
                       sock.send(bytes(" w A ", "ascii"))## is only 4 for testing
                       sock.send(bytes(self.entry_Trigger_signal.get(), "ascii"))
                       sock.send(bytes("\n", "ascii"))
                       time.sleep(0.25)


                if self.entry_Trigger_level.get():
                   print( "got it8")
                   if bluetoothActive == 0:
                       #trigger level
                       x.stdin.write(bytes(mylist[i], "ascii"))
                       x.stdin.write(bytes(" w B ", "ascii"))## is only 4 for testing
                       samples_i = int(self.entry_Trigger_level.get())
                       samples_i_low = samples_i & 0xFF
                       samples_i_high = samples_i >> 8
                       samples_i_low = format(samples_i_low, 'x')
                       samples_i_high = format(samples_i_high, 'x')
                       x.stdin.write(bytes(samples_i_low, "ascii"))
                       x.stdin.write(bytes(" ", "ascii"))
                       x.stdin.write(bytes(samples_i_high, "ascii"))
                       x.stdin.write(bytes("\n", "ascii"))
                       x.stdin.flush()
                       time.sleep(0.25)
                   else :
                       sock.send(bytes(mylist[i], "ascii"))
                       sock.send(bytes(" w B ", "ascii"))## is only 4 for testing
                       samples_i = int(self.entry_Trigger_level.get())
                       samples_i_low = samples_i & 0xFF
                       samples_i_high = samples_i >> 8
                       samples_i_low = format(samples_i_low, 'x')
                       samples_i_high = format(samples_i_high, 'x')
                       sock.send(bytes(samples_i_low, "ascii"))
                       sock.send(bytes(" ", "ascii"))
                       sock.send(bytes(samples_i_high, "ascii"))
                       sock.send(bytes("\n", "ascii"))
                       time.sleep(0.25)


                if self.entry_Trigger.get():
                   print( "got it9")
                   if bluetoothActive == 0:
                       #trigger slope 
                       x.stdin.write(bytes(mylist[i], "ascii"))
                       x.stdin.write(bytes(" w C ", "ascii"))## is only 4 for testing
                       x.stdin.write(bytes(self.entry_Trigger.get(), "ascii"))
                       x.stdin.write(bytes("\n", "ascii"))
                       x.stdin.flush()
                       time.sleep(0.25)
                   else :
                       sock.send(bytes(mylist[i], "ascii"))
                       sock.send(bytes(" w C ", "ascii"))## is only 4 for testing
                       sock.send(bytes(self.entry_Trigger.get(), "ascii"))
                       sock.send(bytes("\n", "ascii"))
                       time.sleep(0.25)




        self.top.destroy()


class Form:

    def __init__(self, master):


        master.title('Data Acquisition Netwrork Controller')
        master.resizable(True, True)
        master.configure(background = '#e1d8b9')

        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#e1d8b9')
        self.style.configure('TButton', background = '#e1d8b9')
        self.style.configure('TLabel', background = '#e1d8b9', font = ('Arial', 11))
        self.style.configure('Header.TLabel', font = ('Arial', 18, 'bold'))

        self.master=master

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack(side=tkinter.TOP, anchor=W)

        ttk.Label(self.frame_content, text = 'Manual I2C Command:').grid(row = 0, column = 0, padx = 5, sticky = 'w')
        ttk.Label(self.frame_content, text = 'Connected Node Addresses:').grid(row = 1, column = 0, padx = 5, sticky = 'w')
        ttk.Label(self.frame_content, text = 'Network State:').grid(row = 2, column = 0, padx = 5, sticky = 'w')
        ttk.Label(self.frame_content, text = 'MCP2221 State:').grid(row = 6, column = 0, padx = 5, sticky = 'w')
        ttk.Label(self.frame_content, text = 'Send Start command to:').grid(row = 4, column = 0, padx = 5, sticky = 'w')
        ttk.Label(self.frame_content, text = 'Retrieve Data from:').grid(row = 3, column = 0, padx = 5, sticky = 'w')

        self.entry_manual = ttk.Entry(self.frame_content, width = 40, font = ('Arial', 10))
        self.entry_report = ttk.Entry(self.frame_content, width = 40, font = ('Arial', 10))
        self.entry_connected = ttk.Entry(self.frame_content, width = 40, font = ('Arial', 10))
        self.entry_netstat = ttk.Entry(self.frame_content, width = 40, font = ('Arial', 10))
        self.entry_mcpstat = ttk.Entry(self.frame_content, width = 40, font = ('Arial', 10))
        self.entry_start = ttk.Entry(self.frame_content, width = 40, font = ('Arial', 10))
        #text_connected_nodes = tkinter.Text(self.frame_content, height=2, width=40).grid(row = 7, column = 0, padx = 5, sticky = 'w')


        #text_connected_nodes.insert(tkinter.END, "hi")

        self.entry_manual.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.entry_report.grid(row = 3, column = 1, padx = 5, pady = 5)
        self.entry_connected.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.entry_netstat.grid(row = 2, column = 1, padx = 5, pady = 5)
        self.entry_mcpstat.grid(row = 6, column = 1, padx = 5, pady = 5)
        self.entry_start.grid(row = 4, column = 1, padx = 5, pady = 5)

        ttk.Button(self.frame_content, text = 'Send',
                   command = self.send).grid(row = 0, column = 2, padx = 5, pady = 5, sticky = 'w')
        ttk.Button(self.frame_content, text = 'Refresh',
                   command = self.refresh).grid(row = 0, column = 3, padx = 5, pady = 5, sticky = 'w')
        
        ttk.Button(self.frame_content, text = 'Start Sampling',
                   command = self.start_sampling).grid(row = 4, column = 2, padx = 5, pady = 5, sticky = 'w')

        ttk.Button(self.frame_content, text = 'Scan',
                   command = self.scan).grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'w')
        ttk.Button(self.frame_content, text = 'Check State',
                   command = self.check_netstat).grid(row = 2, column = 2, padx = 5, pady = 5, sticky = 'w')
##        ttk.Button(self.frame_content, text = 'Check State',
##                   command = self.start_sampling).grid(row = 3, column = 2, padx = 5, pady = 5, sticky = 'w')
        ttk.Button(self.frame_content, text = 'Retrieve',
                   command = self.report).grid(row = 3, column = 2, padx = 5, pady = 5, sticky = 'w')

        ttk.Button(self.frame_content, text = 'Load Setup.txt to Nodes',
                   command = self.load_setup).grid(row = 3, column = 3, padx = 5, pady = 5, sticky = 'w')
        ttk.Button(self.frame_content, text = 'Configure Node(s)',
                   command = self.popup).grid(row = 2, column = 3, padx = 5, pady = 5, sticky = 'w')
        ttk.Button(self.frame_content, text = 'Connect Bluetooth Master',
                   command = self.blueSerial).grid(row = 4, column = 3, padx = 5, pady = 5, sticky = 'w')
        ttk.Button(self.frame_content, text = 'Retrieve CSV Files',
                   command = self.Send_Files).grid(row = 1, column = 3, padx = 5, pady = 5, sticky = 'w')        
        #s = tkinter.Scrollbar(master)
        #T = tkinter.Text(master, height=2, width=40)



        #T.config(yscrollcommand=s.set)

        t = tkinter.Text(master, height=5, width=80)
        t.pack(expand=1, side=tkinter.TOP, fill=tkinter.BOTH)
        #s.pack(side=tkinter.LEFT, fill=tkinter.Y)
        #T.pack(side=tkinter.LEFT, fill=tkinter.Y)
        #s.config(command=t.yview)
        ##create a thread to deal with incoming serial and marcellign the display
        th=Thread(target=reader,args=(x.stdout,linebuffer, t, self))
        th.daemon=True
        th.start()

##
        #also start another thread calling the same function to print all inputs to the other program as made by this one
        #first input box is to be a manual input box, write manual i2c commands


    def send(self):
        print('{}'.format(self.entry_manual.get()))
        if bluetoothActive == 0:
            x.stdin.write(bytes('{}'.format(self.entry_manual.get()), "ascii"))
            x.stdin.write(bytes("\n", "ascii"))
            x.stdin.flush()
        else :
            sock.send(bytes('{}'.format(self.entry_manual.get()), "ascii"))
            sock.send(bytes("\n", "ascii"))


        self.clear()
        ##messagebox.showinfo(title = 'Comand Sender', message = 'Command Sent!')

    def clear(self):
        self.entry_manual.delete(0, 'end')
    def load_setup(self):
        fr.setup_file('SETUP_META_RECORD.txt', x, bluetoothActive, sock)
        
    def scan(self):
        if bluetoothActive == 0:
            x.stdin.write(bytes("52 d \n", "ascii"))
            #x.stdin.write(bytes(" d", "ascii"))
            #x.stdin.write(bytes("\n", "ascii"))
            x.stdin.flush()
        else :
            sock.send(bytes("52 d \n", "ascii"))
            #x.stdin.write(bytes(" d", "ascii"))
            #x.stdin.write(bytes("\n", "ascii"))


    def refresh(self):
        if bluetoothActive == 0:
            x.stdin.write(bytes("\n", "ascii"))
            x.stdin.flush()
        else :
            sock.send(bytes("\n", "ascii"))


    def check_netstat(self):
        global bluetoothActive
        if bluetoothActive == 0:
           x.stdin.write(bytes("52 h \n", "ascii"))
           x.stdin.flush()
        else :
           sock.send(bytes("52 h \n", "ascii"))


    def start_sampling(self):
        #process the input addresses
        string1 = self.entry_start.get()
        mylist = []
        mylist = string1.split(' ')
        print( mylist )
        for i in range(mylist.__len__()):
            #print( mylist[i] )
            if mylist[i] == '':
                print( "danger danger" )
            else:# we can send it add extra checks for non intiger variables
                if bluetoothActive == 0:
                    x.stdin.write(bytes(mylist[i], "ascii"))
                    x.stdin.write(bytes(" w 3\n", "ascii"))## is only 4 for testing
                    x.stdin.flush()
                else :
                    sock.send(bytes(mylist[i], "ascii"))
                    sock.send(bytes(" w 3\n", "ascii"))## is only 4 for testing


                self.clear()
    def report(self):
        string1 = self.entry_report.get()
        mylist = []
        mylist = string1.split(' ')
        print( mylist )
        for i in range(mylist.__len__()):#will have to wait until safe to iterate to next report
            #print( mylist[i] )
            if mylist[i] == '':
                print( "danger danger" )
            else:# we can send it add extra checks for non intiger variables
                if bluetoothActive == 0:
                    x.stdin.write(bytes(mylist[i], "ascii"))
                    x.stdin.write(bytes(" s report\n", "ascii"))## is only 4 for testing
                    x.stdin.flush()
                else :
                    sock.send(bytes(mylist[i], "ascii"))
                    sock.send(bytes(" s report\n", "ascii"))## is only 4 for testing



                self.clear()

    def popup(self):
        self.w=popupWindow(self.master)
        self.master.wait_window(self.w.top)
    def entryValue(self):
        return self.w.value

    ##this needs a better handshake, one that isnt only looking at the serial port hardware, and is nfact listening to the bluetooth slave as well
    def blueSerial(self):
        global addr
        #try accept this too
        if len(sys.argv) < 2:
           print("no device specified.  Searching all nearby bluetooth devices for")
           print("the SampleServer service")
        else:

           addr = sys.argv[1]
           print("Searching for SampleServer on %s" % addr)

        # search for the SampleServer service
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        service_matches = find_service( uuid = uuid, address = addr )

        if len(service_matches) == 0:
            print("couldn't find the SampleServer service =(")
            sys.exit(0)

        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        print("connecting to \"%s\" on %s" % (name, host))

        # Create the client socket
        #sock=BluetoothSocket( RFCOMM ) #made this a global
        sock.connect((host, port))

        global bluetoothActive
        x.kill()  # Send the signal to all the process groups
        bluetoothActive = 1;
    def Send_Files(self):
        sock.send(bytes("Send Files\n", "ascii"))## is only 4 for testing

def main():

    #replace(file_path, pattern, subst)
    #replace('SETUP_META_RECORD.txt', 'Address', 'Address')
    
    #read and send data to child process accordingly from text file
    #this is to be made a button press eventually
    #fr.setup_file('SETUP_META_RECORD.txt', x)
    root = Tk()


    form = Form(root)

    #if linebuffer:
     #print (linebuffer.pop())

    root.mainloop()
    #print ( "oh hello\n\n" )

if __name__ == "__main__": main()
