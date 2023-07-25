from typing import Callable
from gui import BaseGui
from questionData import questionData
import pandas as pd
import os
from ttkbootstrap import ttk, Window, Style
from ttkbootstrap.constants import *
from tkinter import IntVar, StringVar

from utils import ImageFrame
import random



class Game():
    qs = 431
    file_loc = os.path.dirname(__file__)
    save_file = "../data/save.txt"
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
        self.qd = None
        self.save_location = self._create_path(self.save_file)
        self.load_game()

    def make_qdata(self, index: int) -> questionData:
        # takes an index, not a question number
        dat_slide = self.data.iloc[index]
        self.qd = questionData(index, *dat_slide)
        return self.qd

    def random_q(self):
        data = set(list(range(0, self.qs - 1))).difference(self.correct)

        sample = random.sample(list(data), 1)
        print(sample)
        return self.make_qdata(sample[0])
    
    def check_answer(self, num: int) -> bool:
        # use indices instead of question numbers because there are gaps in q no
        
        ind = self.qd.index

        if not ind:
            return
        self.answered.add(ind)
        correct = (self.qd.ans == num)
        if correct:
            self.correct.add(ind)

        return correct
    
    def save_game(self):

        with open(self.save_location, "w") as save:
            save.write(" ".join(str(i) for i in list(self.answered))  + "\n")
            save.write(" ".join(str(i) for i in list(self.correct))  + "\n")
        return

    def load_game(self):
        # do nothing if no savefile has been instantiated
        if not os.path.isfile(self.save_location):
            return
        
        with open(self.save_location, "r") as save:
            line1 = save.readline().strip()
            line2 = save.readline().strip()
            
            if not line1:
                return
            self.answered = set(line1.split(" "))
            self.correct = set(line2.split(" "))


    def get_stats(self):
        return "Stats:\n" + f"Answered: {len(self.answered)}\n" + f"Correct : {len(self.correct)}" 






        
        

class MainGUI(BaseGui):

    def __init__(self, winsize=(800,600)):

        super().__init__(winsize)

        self.q = None # current question

        ## base elements
        self.main_frame = None
        self.curr_label = None
        self.image      = None


        # radiobuttons
        self.opt1       = None
        self.opt2       = None
        self.opt3       = None

        self.result_area = None # did you get it right or wrong


        # buttons and button-related stuff
        self.submit_next = None
        self.skip        = None

        self.response = IntVar(value=-1)

        self.stats       = None
        
        self.game = Game("../data/test.csv")

        self.save_func =   self.game.save_game      

   
        

    def _gen_scene(self):
        
        s = ttk.Style()
        s.configure('.', font=(None, 11))

        # need to start with at least one question
        self.q = self.game.random_q()
        self.main_frame = self.create_frame(self.root, (0,0), (7,3), borderwidth = 1, relief = "solid")
        self.curr_label = self.create_label(self.main_frame, (0, 0), (1, 3), text = self.q.get_question(), padding=20)

        self.generate_responses()

        self.result_area = self.create_label(self.main_frame, (5, 0), (1, 3), text = "", padding=20)
        self.result_area["text"] = ""

        if self.q.has_img:
            self.image = self.create_image(self.main_frame, self.q.img_dir,(1,1), (1,1))
            # print(type(image) == ImageFrame)

        self.submit_next = self.create_button(self.main_frame, grid_plac=(6,0), text = "Submit", command=self.on_submit)
        
        # submit.configure(font = (None, 25))
        self.submit_next.anchor(CENTER)

        self.skip = self.create_button(self.main_frame, grid_plac=(6,1), text = "Skip", command=self.reset_area)
        self.skip.anchor(CENTER)


        self.stats = self.create_label(self.main_frame, grid_plac=(6,2), text = self.game.get_stats())
        self.root.update()

    
        

        super()._gen_scene()
           
        return
    

    def generate_responses(self):
        # can't really loop this anymore, so I unrolled the loop
        response_dict = {0:self.q.opt1, 1:self.q.opt2, 2:self.q.opt3}
                 
        i = 0    
        self.opt1 = self.create_radiobutton(self.main_frame, (i+2,0), (1 ,3 ), text = response_dict[i], padding = 30, variable = self.response, 
                                          value = i+1)
        self.opt1.grid(sticky=W)
        
        i += 1

        self.opt2 = self.create_radiobutton(self.main_frame, (i+2,0), (1 ,3 ), text = response_dict[i], padding = 30, variable = self.response, 
                                          value = i+1)
        self.opt2.grid(sticky=W)


        i += 1

        self.opt3 = self.create_radiobutton(self.main_frame, (i+2,0), (1 ,3 ), text = response_dict[i], padding = 30, variable = self.response, 
                                          value = i+1)
        self.opt3.grid(sticky=W)

    def set_responses(self):
        self.opt1["text"] = self.q.opt1
        self.opt2["text"] = self.q.opt2
        self.opt3["text"] = self.q.opt3

    def on_submit(self):
        if self.submit_next["text"] == "Submit":
            ans = self.response.get()
            if ans == -1:
                self.result_area["text"] = "Please Select an answer"
                self.result_area.update()
                return
            
            correct = self.game.check_answer(ans)
            if correct:
                self.result_area["text"] = "Correct!"
                self.result_area.update()
            else:
                self.result_area["text"] = "Incorrect, answer is:\n" + self.q.get_answer()
                self.result_area.update()

            self.submit_next["text"] = "Next"

        elif self.submit_next["text"] == "Next":
            self.reset_area()
            self.submit_next["text"] = "Submit"

        self.stats["text"] = self.game.get_stats()

    def reset_area(self):
        self.q = self.game.random_q()
        self.curr_label["text"] = self.q.get_question()

        self.set_responses()

       
        self.result_area["text"] = ""

        if self.q.has_img:
            if self.image:
                self.image.destroy()
            self.image = self.create_image(self.main_frame, self.q.img_dir,(1,1), (1,1))
            self.image.resize()
            # print(type(image) == ImageFrame)
        
        self.stats["text"] = self.game.get_stats()
        self.root.update()
        
        
    def run(self, func: Callable = None):
        func = self.save_func
        self._gen_scene()
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            
            if not func:
                pass
            else:
                func()
        finally:
            func()

        


    

test = MainGUI()
test.run()
