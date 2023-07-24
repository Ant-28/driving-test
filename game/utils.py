import tkinter

from ttkbootstrap import ttk, Window
from typing import Any, List

from PIL import Image, ImageTk

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
            
            
            if(type(element) == ttk.Frame):
                self.scale_frame(element, [oldwidth, newwidth, oldheight, newheight])

            if(type(element) == ttk.Label):
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
            itemlist += self.all_children(sub_obj)

        return itemlist
    
    def update_all(self) -> None:
        for child in self.all_children(self.tkobj):
            
            child.update()

    def padding_update(self, object, padding: int):
        self.padding_data[object] = padding

    def image_copy(self, image: Image):
        self.images[image] = image.copy()
        
class ImageFrame(ttk.Frame):
    def __init__(self, image_dir : str, **kwargs):
        self.image_dir = image_dir
        self.image     = Image.open(image_dir)
        self.image_copy = self.image.copy()



        super.__init__(self, **kwargs)

    def resize(self):
        pass


