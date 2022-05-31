from PIL import Image, ImageChops
import os

'''
Concatenate the list of images on each page, and save as PDF


## TO DO
    - Detect and crop only sheet music regions
'''


class Join():
    # folder is a path to a list of images
    def __init__(self, folder, trim = True):
        
        self.images = self.load(folder)
        if trim:
            self.images = [self.trim_img(i) for i in self.images]
        self.page_size = (int(8.5 * 300), int(11 * 300))
        self.images_resized = [self.resize_img(i) for i in self.images]
        self.pages = self.fit_to_pages(self.images_resized)
        
    # Load a list of images
    def load(self, folder):
        images = []
        for i in os.listdir(folder):
            img = Image.open('{}/{}'.format(folder, i))
            images.append(img)
        return images
    
    # Resize images so image width fits page width
    def resize_img(self, img):
        width, height = img.width, img.height
        ratio = self.page_size[0]/width
        return img.resize((int(width * ratio), int(height * ratio)), Image.ANTIALIAS)
    
    # Trim borders around image
    # Stolen from: https://stackoverflow.com/questions/10615901/trim-whitespace-using-pil/10616717#10616717
    def trim_img(self, im, min_white = 700//3):
        corners = [(0,0), (im.size[0]-1, 0), (0, im.size[1]-1), (im.size[0]-1, im.size[1]-1)]
        white_corners = [sum(im.getpixel(c)) >= min_white for c in corners]
        if all(white_corners):
            return im
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)
        
    # Concatenate Resized Images to fit on page size
    def fit_to_pages(self, imgs):
        pages = []
        i = 0
        while i < len(imgs):
            page = Image.new('1', self.page_size)
            acc_height = 0
            while acc_height + imgs[i].height < self.page_size[1]:
                page.paste(imgs[i], (0,acc_height))
                acc_height += imgs[i].height
                i += 1
                if i >= len(imgs): break
            page = page.crop((0, 0, self.page_size[0], acc_height))
            pages.append(page)
        return pages
    
    # Save the file
    def save(self, fname):
        folder = "Sheet Music"
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.pages[0].save('Sheet Music/{}'.format(fname),
                           resolution = 50, save_all = True, append_images=self.pages[1:])
        
        