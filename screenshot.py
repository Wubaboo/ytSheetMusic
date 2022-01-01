import cv2 as cv
import os
from skimage.metrics import structural_similarity as ssim
import numpy as np
import matplotlib.pyplot as plt

'''
Take unique screenshots of frames and extract only the sheet music portions
 of the frames

s = Screenie(video_file, fname = folder_name)
s.take_screenies()
'''
class Screenie():
    def __init__(self, vid_path, fname = 'screenies', thresholding = False, hands = False):
        self.path = vid_path
        
        self.res_path = self.make_folder(fname)
        self.thresholding = thresholding
        self.trim = hands
        
    # Make a new folder "fname"
    def make_folder(self, name = 'screenies'):
        try:
            if not os.path.exists(name):
                os.makedirs(name)
            return name
        except:
            return 'screenies'
    
    # Determines if img1 and img2 are similar (at least a score of thresh)
    def frame_same(self, img1, img2, thresh = 0.9):
        # turn images black and white
        img1_gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        img1_inverse = 255 - img1_gray
        img2_gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY) 
        img2_inverse = 255 - img2_gray
        img1 = cv.threshold(img1_inverse, 250, 255, cv.THRESH_BINARY)[1]
        img2 = cv.threshold(img2_inverse, 250, 255, cv.THRESH_BINARY)[1]
        # Resize images to the same shape, and compare the similarities
        im2 = cv.resize(img2, (img1.shape[1],img1.shape[0]))
        im1 = cv.resize(img1, (img2.shape[1], img2.shape[0]))
        score = max(ssim(img1, im2), ssim(img2, im1))
        #print(score)
        return score >= thresh
    

    # Try extracting the rectangle surrounding the region of interest
    def contours(self, img):
        # Convert to grayscale
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Convert to black and white
        thresh = cv.threshold(gray, 240, 255, cv.THRESH_BINARY)[1]
        # Swap black and white
        #inverse = 255 - thresh
        # Find contours in the image and get the contour with second largest area
        # (First largest contour is the entire frame)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) < 1:
            return img[0:0, 0:0]
        contours = sorted(contours, key = lambda c: cv.contourArea(c))
        largest = contours[-1]
        con_min = largest.min(0)[0]
        con_max = largest.max(0)[0]
        # Crop relevant area
        return img[con_min[1]:con_max[1], con_min[0]:con_max[0]]
        
    ## OBSOLETE
    # Convert img to Black and White
    def grayscale(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        threshold, thresh = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)
        return thresh
    
    ## OBSOLETE
    # Smooth a curve, 
    # https://stackoverflow.com/questions/20618804/how-to-smooth-a-curve-in-the-right-way
    def smooth(self, y, box_pts = 10):
        box = np.ones(box_pts)/box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth
    
    ## OBSOLETE
    # Find the ratio between black and white pixels and coloured pixels
    def bw_ratio(self, im, black = 10, white = 245):
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        
        b_pixels = np.where(gray <= black)
        w_pixels = np.where(gray >= white)
        return (len(b_pixels[0]) + len(w_pixels[0])) / gray.size
    
    ## OBSOLETE 
    # Remove non sheet music portions of the image
    # Tried with horizontal projection, and black and white runs
    def crop_ends(self, im, similar = 1, size_min_ratio = 0.1):
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
        if (cropped.size / im.size) < size_min_ratio:
            return im[0, 0]
        return im[x1:x2, y1:y2]
    
    # Take unique screenshots of the video (frame_same() is used to determine similarity)
    def take_screenies(self, interval = 100, bw_ratio_min = 0.2):
        vid = cv.VideoCapture(self.path)
        
        count = 0
        name_count = 0 
        prev_frame = 0
        while True:
            ret, frame = vid.read()
            # If read incorrectly, break
            if not ret: break
            # for every $interval frames
            if count % interval == 0:
                if self.thresholding:
                    frame = self.grayscale(frame)
                # Remove non sheet music portions
                if self.trim:
                    frame = self.contours(frame)
                    #frame = self.crop_ends(frame)
                # Minimum image size, minimum black white ratio
                if (frame.size >= 1000):
                    # If it's similar to previous frame, ignore
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

# Show an image
def show(ims):
    if isinstance(ims, list):
        for i in range(len(ims)):
            cv.imshow(f'im{i}', ims[i])
    else:
        cv.imshow('im', ims)
    cv.waitKey(0)