from gui import BaseGui
from questionData import questionData
import pandas as pd
import os


class Game():
     
    file_loc = os.path.dirname(__file__)
    def _create_path(self, path: str) -> str:
        path = os.path.join(self.file_loc, path)
        path = os.path.normpath(path)
        return path
    
    def __init__(self, csv_loc: str):
        csv_loc = self._create_path(csv_loc)
        self.data = pd.read_csv(csv_loc)
        # questions answered and correct questions
        self.answered = set()
        self.correct  = set()

    def make_qdata(self, index: int) -> questionData:
        # takes an index, not a question number
        dat_slide = self.data.iloc[index]
        print(dat_slide[0])

        
        

class MainGUI(BaseGui):
    def _gen_scene(self):
        

        return super()._gen_scene()
    


foo = Game("../data/test.csv")
foo.make_qdata(0)
