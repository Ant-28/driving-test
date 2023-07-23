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




if __name__ == "__main__":
    main()