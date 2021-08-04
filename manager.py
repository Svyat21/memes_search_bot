import cv2
import pytesseract
from PIL import Image, ImageChops
import os


def text_scanning(photo):
    scan_photo = cv2.imread(f'MemeLibrary/{photo}.jpg')
    scan_photo = cv2.cvtColor(scan_photo, cv2.COLOR_BGR2RGB)
    scan_res = pytesseract.image_to_string(scan_photo, lang='rus')
    return scan_res


def difference_images(img1, img2):
    with Image.open(f'MemeLibrary/{img1}') as image_1:
        with Image.open(f'MemeLibrary/{img2}') as image_2:
            return ImageChops.difference(image_1, image_2).getbbox()


def check_photo(check_file):
    img_dir = os.listdir('MemeLibrary/')
    for file in img_dir:
        if check_file == file:
            continue
        if difference_images(check_file, file) is None:
            break
    else:
        return True
    return False
