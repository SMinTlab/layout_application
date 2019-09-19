import time

import tkinter as tk
from tkinter import ttk

from log import Log

class Logger:
    
    logs = None

    def __init__(self):
        self.logs = []
        

    def log(self, time, text):
        l = Log(time, text)
        self.logs.append(l)

    def output_reading_speed(self):
        arr = []
        for i,e in enumerate(self.logs):
            if i != 0:
                arr.append(e-self.logs[i-1])
        print(arr)
