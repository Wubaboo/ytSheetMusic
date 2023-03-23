from PIL import Image, ImageChops
import os, psutil
from awsServices import bucket, getFiles, downloadFile, uploadFile
import gc

'''
Concatenate the list of images on each page, and save as PDF
'''

class Join():
    # folder is a path to a list of images
    def __init__(self, folder, trim = True):
        self.folder = folder
        
        if folder not in os.listdir():
            print('getting files')
            self.get_files()
        print('loading folder')
        self.page_size = (int(8.5 * 300), int(11 * 300))
        #self.images = [self.resize_img(self.trim_img(i)) for i in self.load(folder)]
        self.processImages(self.folder)
        print('processed images')
        self.pages = self.fit_to_pages(self.folder)
        print('init done')
        
    def load_image_name(self, folder):
        image_names =[]
        for i in os.listdir(folder):
            if i.endswith('.jpg') and 'processed' in i:
                image_names.append(f'{folder}/{i}')
        return sorted(image_names)
        
    
    def get_files(self):
        files = getFiles(bucket=bucket, prefix=self.folder)
        print(files)
        for folder in files:
            for file in files[folder]:
                object_name = f"{folder}/{file}"
                if not os.path.exists(os.path.dirname(object_name)):
                    os.makedirs(os.path.dirname(object_name), mode=0o777)
                downloadFile(object_name, object_name, bucket)
                print(object_name)
        
    # Load a list of images
    def processImages(self, folder):
        for i in os.listdir(folder):
            if i.endswith('.jpg'):
                prefix, ext = i.split('_')
                new = self.resize_img(self.trim_img(Image.open('{}/{}'.format(folder, i))))
                if new:
                    new.save(f'{folder}/processed_{ext}')
                del new
    
    # Resize images so image width fits page width
    def resize_img(self, img):
        if img:
            width, height = img.width, img.height
            ratio = self.page_size[0]/width
            print(psutil.Process().memory_info().rss/ 1024 ** 2)
            return img.resize((int(width * ratio), int(height * ratio)), Image.LANCZOS)
    
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
    def fit_to_pages(self, folder):
        names = sorted(self.load_image_name(folder))
        print(names)
        pages = []
        i = 0
        while i < len(names):
            page = Image.new('1', self.page_size)
            acc_height = 0
            img = Image.open('{}'.format(names[i]))
            while acc_height + img.height < self.page_size[1]:
                page.paste(img, (0,acc_height))
                acc_height += img.height
                i += 1
                del img
                if i >= len(names): break
                img = Image.open('{}'.format(names[i]))
            page = page.crop((0, 0, self.page_size[0], acc_height))
            blank = Image.new('1', self.page_size, color = 'white')
            padding = (self.page_size[1] - acc_height) // 2
            blank.paste(page, (0, padding))
            del page
            pages.append(blank)
            print(psutil.Process().memory_info().rss/ 1024 ** 2)
        return pages
    
    # Save the file
    def save(self, fname):
        print('saving')
        if not os.path.exists(self.folder):
            os.makedirs(self.folder, mode=0o777)
            
        self.pages[0].save(f"{self.folder}/{fname}",
                           resolution = 300, save_all = True, append_images=self.pages[1:])
        
    def upload_file(self, fname):
        uploadFile(filename = f"{self.folder}/{fname}", bucket=bucket, pdf=True)
        
        