
from __future__ import annotations
import sys

from screeninfo import get_monitors
from ttkbootstrap import ttk, Window
from ttkbootstrap.constants import *
from tkinter import StringVar, Canvas
from utils import WindowTracker
from typing import Tuple, List, Callable


import time

class BaseGui():
    def __init__(self, winsize = (800, 600)):
        # just get the first monitor
        main_mon = get_monitors()[0]
        self.scrn_width = main_mon.width
        self.scrn_height = main_mon.height
        self.winsize = winsize

        # things that init window will handle

        self.root = None
        # windowtracker
        self.wt   = None

        self._init_window()
        



    def _init_window(self):
        coords = self.get_center(self.scrn_width, self.scrn_height, *self.winsize)
        # take a fraction of screen height for window width
        # ttkbootstrap supports hidpi by default, thank goodness
        self.root = Window(title = "Driving Test v0.1", themename="darkly", size = self.winsize, position=coords)
        self.root.update() # update root data and never forget this for the love of god
        self.wt = WindowTracker(self.root)

        

        


    # get coords for center of screen
    def get_center(self, scrn_width: int, scrn_height: int, win_width:int, win_height: int):

        left_corner = scrn_width // 2 - win_width // 2
        top_corner = scrn_height // 2 - win_height // 2
        return (left_corner, top_corner)
    
    def create_frame(self, parent: Window, grid_plac: Tuple[int, int] = (0, 0),
                                           grid_data: Tuple[int, int] = (1, 1),  **kwargs) -> ttk.Frame:

        w = self.wt.width if "width" not in kwargs else kwargs["width"]
        h = self.wt.height if "height" not in kwargs else kwargs["height"]
        
        f = ttk.Frame(parent, width=w, height=h,  **kwargs)

        col, row = grid_plac
        ncols, nrows = grid_data

        f.grid(column=col, row=row, columnspan=ncols, rowspan=nrows)
        f.grid_propagate(False)
        f.grid_columnconfigure(index = tuple(range(ncols)), weight=1, uniform="column")
        f.grid_rowconfigure(   index = tuple(range(nrows)), weight=1, uniform="row"   )
        return f



    def _gen_scene(self):
        # the function you should edit when creating a scene
        
        pass
        
        
        
        
        


    def run(self, func: Callable = None):
        
        self._gen_scene()
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            
            if not func:
                pass
            else:
                func()


def main():
    main_obj = BaseGui()
    
    main_obj.run()


if __name__ == "__main__":
    main()






# winframe = ttk.Frame(root, width = scrn_width, height = scrn_height, padding=0,
#                      borderwidth=1, relief='solid')
# winframe.grid(column=0, row=0, columnspan=3, rowspan=3,sticky=())
# winframe.grid_propagate(False)
# winframe.grid_columnconfigure((0,1,2), weight = 1, uniform="column")
# winframe.grid_rowconfigure((0,1,2), weight = 1, uniform="row")



# meters = StringVar()


# def task():
#     meters.set("AA")
#     root.update()

#     root.after(3000)

#     meters.set("B")
#     root.update()

# for i in range(3):
#     for j in range(3):
#         x, y, w, h = winframe.grid_bbox(i,j)

#         label = ttk.Label(winframe, textvariable=meters, borderwidth = 1, relief = "solid", width = w,
#        )
#         label.grid(column=i, row=j, ipadx=scrn_width//3, ipady=scrn_height//3, sticky=N)
      
#         label.grid_propagate(False)
#         label.configure(anchor="center")

        
        
# # for child in winframe.winfo_children(): 
# #     child.grid_configure(padx=5, pady=5, ipadx=100, ipady=100)


# task()
# root.mainloop()
