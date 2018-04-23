#!/usr/bin/python3
# feedback_solution.py by Barron Stone
# This is an exercise file from Python GUI Development with Tkinter on lynda.com
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
import dnsmanager as dns

linebuffer=[] #buffer used to store and print serial data
                
class Form:

    def __init__(self, master):

        
        master.title('Domain Name Information Extractor')
        master.resizable(True, True)
        master.configure(background = '#e1d8b9')
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#e1d8b9')
        self.style.configure('TButton', background = '#e1d8b9')
        self.style.configure('TLabel', background = '#e1d8b9', font = ('Arial', 11))
        self.style.configure('Header.TLabel', font = ('Arial', 18, 'bold'))
        
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack(side=tkinter.TOP, anchor=W)

        ttk.Label(self.frame_content, text = 'Enter Domain Name').grid(row = 0, column = 0, padx = 5, sticky = 'w')
        ttk.Label(self.frame_content, text = 'Enter Domain IPV4 Address').grid(row = 1, column = 0, padx = 5, sticky = 'w')
        
        self.entry_manual = ttk.Entry(self.frame_content, width = 24, font = ('Arial', 10))
        self.entry_report = ttk.Entry(self.frame_content, width = 24, font = ('Arial', 10))

        #text_connected_nodes = tkinter.Text(self.frame_content, height=2, width=40).grid(row = 7, column = 0, padx = 5, sticky = 'w')

        
        #text_connected_nodes.insert(tkinter.END, "hi")
        
        self.entry_manual.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.entry_report.grid(row = 1, column = 1, padx = 5, pady = 5)

        
        ttk.Button(self.frame_content, text = 'Send',
                   command = self.send).grid(row = 0, column = 2, padx = 5, pady = 5, sticky = 'w')

        ttk.Button(self.frame_content, text = 'Send',
                   command = self.send_ipv4).grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'w')

        #t = tkinter.Text(master, height=5, width=80)
        #t.pack(expand=1, side=tkinter.TOP, fill=tkinter.BOTH)

        self.text = Text(master)
        scroll = Scrollbar(master)
        self.text.focus_set()

        scroll.pack(side=RIGHT, fill=Y)
        self.text.pack(side=LEFT, fill=Y)

        scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=scroll.set)

        #t.insert(tkinter.END, "what hte")
        

    def send(self):
       # print(inteter)
        print('{}'.format(self.entry_manual.get()))
        #t.insert(tkinter.END, '{}'.format(self.entry_manual.get()))
        #t.insert(tkinter.END, "what hte")
        input0 = "eait.uq.edu.au"
        input1 = "remote.labs.eait.uq.edu.au"
        input2 = "microsoft.com"
        input3 = "130.102.71.160"
        input4 = "130.102.79.33"
        input5 = "mail.google.com"

        inpuuut = '{}'.format(self.entry_manual.get())
        dns_flag = 1

        response = dns.send_udp_message(dns.process_input(inpuuut, dns_flag, 0), "8.8.8.8", 53)

        # process the response to extract the information

        self.text.insert(END, dns.process_canonical(response, inpuuut) + "\n")

        self.text.insert(END, dns.process_response_ipv4(response, 1, dns.process_input(inpuuut, dns_flag, 0)) + "\n")

        response = dns.send_udp_message(dns.process_input(inpuuut, dns_flag, 1), "8.8.8.8", 53)

        # process the response to extract the information

        self.text.insert(END, dns.process_response_ipv4(response, 0, dns.process_input(inpuuut, dns_flag, 1)) + "\n")


    def send_ipv4(self):

        inpuuut = '{}'.format(self.entry_report.get())
        dns_flag = 0

        response = dns.send_udp_message(dns.process_input(inpuuut, dns_flag, 0), "8.8.8.8",
                                    53)  # "2001:4860:4860::8888" ipv6 server

        self.text.insert(END, dns.process_host_name_reverse(response) + "\n")


def main():            

    
    root = Tk()


    form = Form(root)
    
    root.mainloop()
    
    
if __name__ == "__main__": main()
