'''
Created on 27-jul.-2014

@author: Simon
'''
import time

import Tkinter as tk
import frontend
from python_runtime.statecharts_core import Event


if __name__ == '__main__':
    controller = frontend.Controller()
    controller.start()
    myinstance = None
    for i in controller.object_manager.instances_map.iterkeys():
        if isinstance(i, tk.Tk):
            myinstance = i
    if myinstance:
        myinstance.mainloop()
