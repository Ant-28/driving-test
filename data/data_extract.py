from PyPDF2 import PdfReader
from tabula import read_pdf
from typing import List, Tuple
import re # regexes my beloved

import pandas as pd
from pandas import DataFrame
import numpy as np
# grammar corrections
import pkg_resources
from symspellpy.symspellpy import SymSpell


## symspell boilerplate to handle typos and missing spaces
## I have unabashedly copied this from their documentation

# Set max_dictionary_edit_distance to avoid spelling correction
sym_spell = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt"
)
# term_index is the column of the term and count_index is the
# column of the term frequency
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)


########## end boilerplate here

# The only reason to use pyPDF2
reader = PdfReader("testfile.pdf")
npages = len(reader.pages)


concat_df = DataFrame()
df_list = []
for pg_no in range(1,npages + 1):
    # first page has a header
    pdopts = {"header": None} if pg_no > 1 else None
    new_df = read_pdf("testfile.pdf", lattice=True, pages=pg_no, pandas_options=pdopts)
    #  print(new_df[0].shape[0])
    new_df[0].columns = ["q_no", "question", "opt1", "opt2", "opt3", "ans", "img"]
    df_list += new_df
    # new_df 0 is the dataframe, new_df is a list of dataframes


concat_df = pd.concat(df_list, ignore_index=True)

# clean up columns


replace_list = [("\r", " "),
                ("_x000D_", ""),
                (r"\s{2,}", " "),
                (r"\.+", ""),
                (r"\s+\?", r"?"),
]


def column_cleanup(in_str: str, replace_list: List[Tuple[str, str]] = replace_list) -> str:
    # take in a string and replace any instances of the items in replace list
    
    for replac in replace_list:
        in_str = re.sub(replac[0], replac[1], in_str)
    
    in_str_data = sym_spell.word_segmentation(in_str)
        
    return in_str_data.corrected_string.strip()    

# max length of 222

for column in [ "question", "opt1", "opt2", "opt3"]:
    concat_df[column] = concat_df[column].apply(column_cleanup)

## add image location

#### image indices generation
# this part is done manually
# image 420 uses 246

image_ind = []

# questions 1 - 158 have a pattern of questions with an image every even question
for i in range(79):
    image_ind.append(2*(i+1))

# add image 420
# we only need the indices now
image_ind += [243, 246, 255, 256, 258, 333, 375, 
                     420, 426, 429, 430, 431, 432, 434, 435, 436]




### end image indices generation (to match the question number)

concat_df["img"] = concat_df["img"].to_string(na_rep = "")
print(type(concat_df["img"]))


# lambda abuse
concat_df["img"] = concat_df["q_no"].apply(lambda x: "images/image_" + str(baz) \
                                               if (x in image_ind) and (baz := image_ind[image_ind.index(x)]) else "")
concat_df.info()

concat_df.to_csv('test.csv', index=False)
