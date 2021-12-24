import cv2 as cv
import os
from skimage.metrics import structural_similarity as ssim
import numpy as np
import matplotlib.pyplot as plt

'''
Take unique screenshots of every 100 frames

s = Screenie(video_file, fname = folder_name)
s.take_screenies()
'''
class Screenie():
    def __init__(self, vid_path, fname = 'screenies', thresholding = False):
        self.path = vid_path
        
        self.res_path = self.make_folder(fname)
        self.thresholding = thresholding
        
    # Make a new folder "fname"
    def make_folder(self, name = 'screenies'):
        try:
            if not os.path.exists(name):
                os.makedirs(name)
            return name
        except:
            return 'screenies'
            
    
    # Determines if img1 and img2 are similar (at least a score of thresh)
    def frame_same(self, img1, img2, thresh = 0.87):
        return (img1.shape == img2.shape) and (ssim(img1, img2, multichannel = True) >= thresh)
        try:
            return (img1.shape == img2.shape) and (ssim(img1, img2, multichannel = True) >= thresh)
        except:
            print("error determining img similarity")
    
    # Convert img to Black and White
    def grayscale(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        threshold, thresh = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)
        return thresh
    
    # Smooth a curve, 
    # https://stackoverflow.com/questions/20618804/how-to-smooth-a-curve-in-the-right-way
    def smooth(self, y, box_pts = 10):
        box = np.ones(box_pts)/box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth
    
    # Find the ratio between black and white pixels and coloured pixels
    def bw_ratio(self, im, black = 10, white = 245):
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        
        b_pixels = np.where(gray <= black)
        w_pixels = np.where(gray >= white)
        return (len(b_pixels[0]) + len(w_pixels[0])) / gray.size
        
    def crop_ends(self, im, similar = 0.05, size_min_ratio = 0.3):
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        thresh = cv.threshold(gray, 254, 255, cv.THRESH_BINARY)
        inverse = 255 - thresh[1]
         
        vert_proj = np.sum(inverse, 0)
        hori_proj = np.sum(inverse, 1)
        plt.plot(vert_proj)
        plt.plot(hori_proj)

        vert_mins = np.where(vert_proj < vert_proj.min() * (1 + similar))
        hori_mins = np.where(hori_proj < hori_proj.min() * (1 + similar))
        x1, x2 = hori_mins[0].min(), hori_mins[0].max()
        y1, y2 = vert_mins[0].min(), vert_mins[0].max()
        
        cropped = im[x1:x2, y1:y2]
        if (cropped.size / gray.size) > size_min_ratio:
            
        return im[x1:x2, y1:y2]
    
    def prop_of_screen()
    # Take unique screenshots of the video (frame_same() is used to determine similarity)
    def take_screenies(self, interval = 50, bw_ratio_min = 0.3):
        vid = cv.VideoCapture(self.path)
        
        count = 0
        name_count = 0 
        prev_frame = 0
        while True:
            ret, frame = vid.read()
            if not ret: break
            if count % interval == 0:
                if self.thresholding:
                    frame = self.grayscale(frame)
                frame = self.crop_ends(frame)
                if (frame.size >= 5000) and (self.bw_ratio(frame) > bw_ratio_min):
                    if ((isinstance(prev_frame, int)) or (not self.frame_same(frame, prev_frame))):
                        name = self.res_path + '/frame_{}.jpg'.format(str(name_count).zfill(2))
                        print("Creating ", name)
                        print(count)
                        cv.imwrite(name, frame)
                        prev_frame = frame
                        name_count += 1
            count += 1
            
        vid.release()
        cv.destroyAllWindows()

def show(ims):
    if isinstance(ims, list):
        for i in range(len(ims)):
            cv.imshow(f'im{i}', ims[i])
    else:
        cv.imshow('im', ims)
    cv.waitKey(0)