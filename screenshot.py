import cv2 as cv
import os
from skimage.metrics import structural_similarity as ssim

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
    def frame_same(self, img1, img2, thresh = 0.9):
        try:
            return ssim(img1, img2, multichannel = True) >= thresh
        except:
            print("error determining img similarity")
    
    # Convert img to Black and White
    def grayscale(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        threshold, thresh = cv.threshold(gray, 254, 255, cv.THRESH_BINARY)
        return thresh
    
    # Take unique screenshots of the video (frame_same() is used to determine similarity)
    def take_screenies(self, interval = 100):
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
                if (isinstance(prev_frame, int)) or (not self.frame_same(frame, prev_frame)):
                    name = self.res_path + '/frame_{}.jpg'.format(str(name_count).zfill(2))
                    print("Creating ", name)
                    print(count)
                    cv.imwrite(name, frame)
                    prev_frame = frame
                    name_count += 1
            count += 1
            
        vid.release()
        cv.destroyAllWindows()
