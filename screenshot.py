import cv2 as cv
import os, psutil
from skimage.metrics import structural_similarity as ssim
import numpy as np
from awsServices import bucket, uploadFile

'''
Take unique screenshots of frames and extract only the sheet music portions
 of the frames

s = Screenie(video_file, fname = folder_name)
s.take_screenies()
'''
class Screenie():
    def __init__(self, vid_path, fname = 'screenies', hands = False, threshold = 0.9):
        self.path = vid_path
        
        self.res_path = self.make_folder(fname)
        self.threshold = threshold
        self.trim = hands
    
    def upload_images(self):
        for file in os.listdir(self.res_path):
            uploadFile(filename = f"{self.res_path}/{file}", bucket=bucket)
            
    # Make a new folder "fname"
    def make_folder(self, name = 'screenies'):
        try:
            if not os.path.exists(name):
                os.makedirs(name, mode=0o777)
            return name
        except:
            return 'screenies'
    
    # Determines if img1 and img2 are similar (at least a score of thresh)
    def frame_same(self, img1, img2, thresh = None):
        if not thresh:
            thresh = self.threshold
        # turn images black and white
        img1_gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        print('cvt1')
        img1_inverse = 255 - img1_gray
        img2_gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY) 
        print('cvt2')
        img2_inverse = 255 - img2_gray
        img1 = cv.threshold(img1_inverse, 150, 255, cv.THRESH_BINARY)[1]
        print('thresh1')
        img2 = cv.threshold(img2_inverse, 150, 255, cv.THRESH_BINARY)[1]
        print('thresh2')
        # Resize images to the same shape, and compare the similarities
        im2 = cv.resize(img2, (img1.shape[1],img1.shape[0]))
        print('resize1')
        im1 = cv.resize(img1, (img2.shape[1], img2.shape[0]))
        print('resize2')
        score = max(ssim(img1, im2), ssim(img2, im1))
        print(score)
        return score >= thresh
    
    
    '''TRY RELATIVE AREAS OF BOUNDED RECTANGLES'''
    # Try extracting the rectangle surrounding the region of interest
    def contours(self, img):
        # Convert to grayscale
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Convert to black and white
        thresh = cv.threshold(gray, 240, 255, cv.THRESH_BINARY)[1]
        # Swap black and white
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
    
    # Find the ratio between black and white pixels and coloured pixels
    def bw_ratio(self, im, black = 10, white = 245):
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        b_pixels = np.where(gray <= black)
        w_pixels = np.where(gray >= white)
        return (len(b_pixels[0]) + len(w_pixels[0])) / gray.size
    
    # Take unique screenshots of the video (frame_same() is used to determine similarity)
    def take_screenies(self, interval = 100, bw_ratio_min = 0.05):
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
                # Remove non sheet music portions
                print('in count%interval')
                if self.trim:
                    frame = self.contours(frame)
   
                print('bwratio', self.bw_ratio(frame))
                # Minimum image size, minimum black white ratio
                if (frame.size >= 1000) and (self.bw_ratio(frame) > bw_ratio_min):
                    # If it's similar to previous frame, ignore
                    if ((isinstance(prev_frame, int)) or (not self.frame_same(frame, prev_frame))):
                        name = self.res_path + '/frame_{}.jpg'.format(str(name_count).zfill(3))
                        print(f"Creating {name} at frame {count}")
                        cv.imwrite(name, frame)
                        os.chmod(name, 0o777)
                        prev_frame = frame
                        name_count += 1
                        print(psutil.Process().memory_info().rss/ 1024 ** 2)
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