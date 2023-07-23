from tkinter import * 
from ttkbootstrap import ttk, Window
from typing import List

class WindowTracker():
    def __init__(self, tk: Tk | Window):
        self.tkobj = tk
    
        self.width = tk.winfo_width()
        self.height = tk.winfo_height()


    def scale_objects(self, event: Event):
        obj = event.widget # get widget
        if(type(obj) != type(self.tkobj) ):
            return
        oldwidth, oldheight = self.width, self.height
        newwidth, newheight = event.width, event.height
        self.width, self.height = newwidth, newheight
        
        for element in obj.winfo_children():
            # print(type(element))
            
            if(type(element) == ttk.Frame):
                self.scale_frame(element, [oldwidth, newwidth, oldheight, newheight])
               
        self.tkobj.update()

    def scale_frame(self, frame: Frame, width_height: List):
        assert(len(width_height) == 4)
        ew, eh = frame.winfo_width(), frame.winfo_height()
        ow, nw, oh, nh = width_height
        # lots of multiplications and divisions otherwise you get floating point
                # imprecision
        frame.configure(width = round(ew * nw/ow, 0),
                        height = round(eh * nh/oh, 0))


    

