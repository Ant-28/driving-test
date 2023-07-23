# based on: https://pythonscholar.com/extract-images-from-pdf-in-python/
import fitz
import os
import io
from PIL import Image
import shutil



# this is such a manual task that a class wouldn't generalize much
# dear reader, tell me, is this a good idea? (I need help)


# base image extraction class

class ImageExtract():
    # script location
    file_loc = os.path.dirname(__file__)

    def __init__(self, pdf_path: str, image_dir: str) -> None:
        # self.file_path = file_path
        self.image_dir = self._create_path(image_dir)
        self.pdf_file  = fitz.open(self._create_path(pdf_path))
        self.pages = len(self.pdf_file)
        # you're free to create the image index dictionary however you want (for naming purposes)
        self.index_dict = {}
        self.imgname_list = []

        self.create_index_dict()
        self.create_imgname_list()

        self.default_num_gen = self._def_n_gen()

   

    def create_index_dict(self):
        # user-defined
        pass

    def create_imgname_list(self, remove_dup: bool = True):
                # image list
        self.imgname_list = []

        for pg_no in range(self.pages):
            # get one page
            page = self.pdf_file[pg_no]
            self.imgname_list += page.get_images()

        # remove duplicates
        if remove_dup:
            self.imgname_list = list(set(self.imgname_list))

        self.sort_imgname_list()

    def sort_imgname_list(self):
        return self.imgname_list

    def export_images(self):
        
        for ind in range(len(self.imgname_list)):

            # get xref
            img = self.imgname_list[ind]
            xref = img[0]
            base_img = self.pdf_file.extract_image(xref)
            # get image bytes and extensions
            img_bytes = base_img["image"]
            img_ext   = base_img["ext"]

            # you can pass in file-like objects to Image.open
            image = Image.open(io.BytesIO(img_bytes))

            self.save_image(image, img_ext)

    def save_image(self, image: Image, image_ext: str, image_str: str = None):
            ## user-defined, default implementation here
            if not image_str:
                image_str = "img_" + self.default_num_gen.__next__() # get next value of generator
            # add extension by default
            image_str += f".{image_ext}"
            image_str = os.path.join(self.image_dir, image_str)
           
            image.save(open(image_str, "wb"))
            
    
    def copy_image(self, old_image: str, new_image: str):
        # create a copy of an image, basically uses 
        # assume a relative path
        old_image = self._create_path(old_image)
        new_image = self._create_path(new_image)

        shutil.copy(old_image, new_image) # let the user handle  relative paths

    def _def_n_gen(self):
        x = 0
        while True:
            yield x
            x += 1
        
    def _create_path(self, path: str) -> str:
        path = os.path.join(self.file_loc, path)
        path = os.path.normpath(path)
        return path
    

            





# handle the case of img_420