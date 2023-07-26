import pandas
import numpy as np
import os

class questionData():
    file_loc = os.path.dirname(__file__)
    def __init__(self, index: int, no: int, 
                 q: str, opt1: str, opt2: str, opt3: str, 
                 ans: int, img_dir: str = None):
        self.index = index
        self.no = no
        self.q  = q
        self.opt1, self.opt2, self.opt3 = opt1, opt2, opt3
        self.ans = ans
       
        
        # nan is a float so img only exists iff img_dir is a string
        self.has_img = True if type(img_dir) == str else False

        if self.has_img:
            self.img_dir = self._create_path(img_dir)

    def ask_question(self) -> bool:
        print(f"Question {self.no}: ")
        print(self.q)

        print("\nOptions: ")
        print("1:", self.opt1)
        print("2:", self.opt2)
        print("3:", self.opt3)

        ans = input("Select an answer: \n").strip()
        while ans not in ["1", "2", "3"]:
             
            print("Invalid answer. Select a number between 1 - 3")

        if int(ans) == self.ans:
            print("Correct!")
            return True
        else:
            print("Incorrect, the answer is:", self.get_answer())
            return False
        
    def get_answer(self) -> str:
        ans_dict = {1:self.opt1, 2:self.opt2, 3:self.opt3}
        return ans_dict[self.ans]

    def get_question(self) -> str:
        return f"Question {self.no}:\n{self.q}"
    
    def _create_path(self, path: str) -> str:
        path = os.path.join(self.file_loc, path)
        path = os.path.normpath(path)
        return path