# based on: https://pythonscholar.com/extract-images-from-pdf-in-python/
import fitz
import os
import io
from PIL import Image


#### image indices generation
# this part is done manually
# image 420 uses 246

image_ind = {}

# questions 1 - 158 have a pattern of questions with an image every even question
for i in range(79):
    image_ind[i] = 2*(i+1)

# this part has to be done by hand
other_img_indices = [243, 246, 255, 256, 258, 333, 375, 
                     426, 429, 430, 431, 432, 434, 435, 436]

for i in range(79, 79 + len(other_img_indices)):
    image_ind[i] = other_img_indices[i-79]


### end image indices generation (to match the question number)




file_path = "testfile.pdf"

pdf_file  = fitz.open(file_path)
pages = len(pdf_file)


imgs_path = "images/"

# image list
img_list = []

for pg_no in range(pages):
    # get one page
    page = pdf_file[pg_no]
    img_list += page.get_images()


# remove duplicates
img_list = list(set(img_list))

# the images are saved as im{num} so we need to extract and sort by the number to see 
# the images in the correct order
img_list = sorted(img_list, key = lambda x : int(x[7][2:]))

for ind in range(len(img_list)):
    img = img_list[ind]
    xref = img[0]
    base_img = pdf_file.extract_image(xref)
    # get image bytes and extensions
    img_bytes = base_img["image"]
    img_ext   = base_img["ext"]

    # you can pass in file-like objects to Image.open
    image = Image.open(io.BytesIO(img_bytes))
    
    # write bytes
    # question
    q = image_ind[ind]
    image.save(open(imgs_path+f"image_{q}.{img_ext}", "wb"))

    if q == 246:
        image.save(open(imgs_path+f"image_420.{img_ext}", "wb"))


# handle the case of img_420