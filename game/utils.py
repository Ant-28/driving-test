import tkinter

from ttkbootstrap import ttk, Window
from typing import Any, List
from typing import Type
from PIL import Image, ImageTk
from math import floor

# source: https://stackoverflow.com/questions/24061099/tkinter-resize-background-image-to-window-size
class ImageFrame(ttk.Frame):
    def __init__(self, parent, image_dir : str, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.image_dir = image_dir
        self.image     = Image.open(image_dir)
        self.image_copy = self.image.copy()

        self.image_tk = ImageTk.PhotoImage(self.image)
        self.label    = ttk.Label(self,  image = self.image_tk)
        
        img_width = self.image.width
        img_height = self.image.height

        
        self.label.pack(fill="none")


        self.ar = self.image.width/self.image.height
        
        

    def resize(self):
        
        
        self.update()
         # ew, eh = self.image.width, self.image.height
        # ow, nw, oh, nh = scaling_data
        
        # initialize outside scope
        new_height = 0
        new_width = 0
        # please don't try to simplify this with intermediate variables
        # I assure you that floating point imprecisions will make your life a living hell
        # get grid information to scale image

        grid_info = self.grid_info()
        row, col = grid_info["row"], grid_info["column"]
        grid_data = self.master.grid_bbox(row, col)

        print(grid_data)
        # get grid width and height
        grid_width = grid_data[2]
        grid_height = grid_data[3]

        new_width = 0
        new_height = 0

        # scale to width if wide, scale to grid height if tall
        
        new_width1 = grid_width
        new_height1 = int(new_width1/self.ar)
        
        new_height2 = grid_height
        new_width2 = int(new_height2*self.ar)

        if new_width1 <= grid_width and new_height1 <= grid_height:
            new_width, new_height = new_width1, new_height1
        else:
            new_width, new_height = new_width2, new_height2


        print(new_width, new_height)              
        # keep the original copy as is 
        self.image = self.image_copy.resize((new_width, new_height))
        print(new_width, new_height)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.label.configure(image = self.image_tk)
        self.label.pack(fill="both")
        self.label.update()
        self.update()


class WindowTracker():
    def __init__(self, tk: tkinter.Tk | Window, padding_data: dict):
        self.tkobj = tk
        self.tkobj.bind("<Configure>", self.scale_objects)
        
        
        self.width = tk.winfo_width()
        self.height = tk.winfo_height()
        self.padding_data = {}
        self.images = {} # store an image and its copy

        


    def scale_objects(self, event: tkinter.Event):
        obj = event.widget # get widget
        if(type(obj) != type(self.tkobj) ):
            return
        oldwidth, oldheight = self.width, self.height
        newwidth, newheight = event.width, event.height
        self.width, self.height = newwidth, newheight
        
        for element in self.all_children(obj):
            
            if(type(element) == ImageFrame):
                self.scale_imframe(element,[oldwidth, newwidth, oldheight, newheight])
            elif(type(element) == ttk.Frame):
                self.scale_frame(element, [oldwidth, newwidth, oldheight, newheight])

            elif(type(element) == ttk.Label):
                self.scale_text(element)
               
        self.tkobj.update()

    def scale_frame(self, frame: ttk.Frame, width_height: List):
        assert(len(width_height) == 4)
        ew, eh = frame.winfo_width(), frame.winfo_height()
        ow, nw, oh, nh = width_height
        # lots of multiplications and divisions otherwise you get floating point
                # imprecision
        frame.configure(width = round(ew * nw/ow, 0),
                        height = round(eh * nh/oh, 0))
        
    def scale_imframe(self, frame: Type[ImageFrame], width_height: List):
        assert(len(width_height) == 4)
        self.scale_frame(frame, width_height)
        frame.resize() # the class can do the heavy lifting
        
    def scale_text(self, label: ttk.Label):
        label_parent = label.master
        label_parent.update()
        padding = self.padding_data[label]

    
        label["wraplength"] = label_parent.winfo_width() - padding
        label.update()
        return


    def all_children(self, obj) -> List:
        # get all children of an object in tkinter
        itemlist = []
        if not obj.winfo_children():
            return []

        

        for sub_obj in obj.winfo_children():
            itemlist.append(sub_obj)

            if type(obj) != ImageFrame:
                itemlist += self.all_children(sub_obj)

        return itemlist
    
    def update_all(self) -> None:
        for child in self.all_children(self.tkobj):
            
            child.update()

    def padding_update(self, object, padding: int):
        self.padding_data[object] = padding

    def image_copy(self, image: Image):
        self.images[image] = image.copy()
        

        


        
        


