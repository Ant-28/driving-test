from gui import BaseGui
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
        





class MainGUI(BaseGui):
    def _gen_scene(self):


        return super()._gen_scene()