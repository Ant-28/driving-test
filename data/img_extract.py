from PIL import Image
from _img_extract import ImageExtract


# Image Extraction for driving test
class DrivingTestImgExt(ImageExtract):
    def create_index_dict(self):
        ## assume keys are all continuous nonnegative integers that are less than the size of the dictionary
        #### image indices generation
        # this part is done manually
        # image 420 uses 246

        self.index_dict = {}

        # questions 1 - 158 have a pattern of questions with an image every even question
        for i in range(79):
            self.index_dict[i] = 2*(i+1)

        # this part has to be done by hand
        other_img_indices = [243, 246, 255, 256, 258, 333, 375, 
                            426, 429, 430, 431, 432, 434, 435, 436]

        for i in range(79, 79 + len(other_img_indices)):
            self.index_dict[i] = other_img_indices[i-79]
            
        ### end image indices generation (to match the question number)

    def sort_imgname_list(self):
        self.imgname_list = sorted(self.imgname_list, key = lambda x : int(x[7][2:])) 

    def save_image(self, image: Image, image_ext: str, image_str: str = None):
        index = self.default_num_gen.__next__()
        image_str = "image_" + str(self.index_dict[index])
        return super().save_image(image, image_ext, image_str)
# original code


    
def main():
    file_path = "testfile.pdf"
    image_dir = "../images"
    img_extractor = DrivingTestImgExt(file_path, image_dir)
    img_extractor.export_images()
    img_extractor.copy_image("../images/image_246.jpeg", "../images/image_420.jpeg")






file_path = os.path.join(os.path.dirname(__file__), file_path)
pdf_file  = fitz.open(file_path)

pages = len(pdf_file)

img_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../images/"))

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
    # print(image.)
    
    # write bytes
    # question
    q = image_ind[ind]

    print(os.path.join(img_path,f"image_{q}.{img_ext}"))
    image.save(open(os.path.join(img_path,f"image_{q}.{img_ext}"), "wb"))

    if q == 246:
        image.save(open(os.path.join(img_path,f"image_420.{img_ext}"), "wb"))