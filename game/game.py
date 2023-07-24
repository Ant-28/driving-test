from gui import BaseGui
from questionData import questionData
import pandas as pd
import os
from ttkbootstrap import ttk, Window
from ttkbootstrap.constants import *
from tkinter import IntVar, StringVar
import random



class Game():
    qs = 431
    file_loc = os.path.dirname(__file__)
    def _create_path(self, path: str) -> str:
        path = os.path.join(self.file_loc, path)
        path = os.path.normpath(path)
        return path
    
    def __init__(self, csv_loc: str):
        csv_loc = self._create_path(csv_loc)
        self.data = pd.read_csv(csv_loc, na_values="-")
        # questions answered and correct questions
        self.answered = set()
        self.correct  = set()

    def make_qdata(self, index: int) -> questionData:
        # takes an index, not a question number
        dat_slide = self.data.iloc[index]
        qd = questionData(*dat_slide)
        return qd

    def random_q(self):
        return self.make_qdata(random.randint(0, self.qs - 1))
        
        

class MainGUI(BaseGui):

    def __init__(self, winsize=(800,600)):

        super().__init__(winsize)

        self.q = None
        self.main_frame = None
        self.response = IntVar()

    def _gen_scene(self):
        
        
        foo = Game("../data/test.csv")

        
        self.q = foo.make_qdata(0)

        
        

        self.main_frame = self.create_frame(self.root, (0,0), (6,3), borderwidth = 1, relief = "solid")
        
        curr_label = self.create_label(self.main_frame, (0, 0), (1, 3), text = self.q.get_question(), padding=20)
        
        self.generate_responses()
        
        if self.q.has_img:
            pass
        
        self.root.update()
        

        super()._gen_scene()
           
        return
    

    def generate_responses(self):
        response_dict = {0:self.q.opt1, 1:self.q.opt2, 2:self.q.opt3}
        for i in range(3):
            opt = self.create_radiobutton(self.main_frame, (i+2,0), (1 ,3 ), text = response_dict[i], padding = 30, variable = self.response, 
                                          value = i+1)
            opt.grid(sticky=W)
        


    

test = MainGUI()
test.run()
