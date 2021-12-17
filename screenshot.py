import cv2 
import os
import time
from skimage.metrics import structural_similarity as ssim

class Screenie():
    def __init__(self, vid_path, fname = 'screenies'):
        self.path = vid_path
        
        self.res_path = self.make_folder(fname)
    
    
    def make_folder(self, name = 'screenies'):
        try:
            if not os.path.exists(name):
                os.makedirs(name)
                return name
        except:
            print("error making '{}' folder".format(name))
    
    # Determines if img1 and img2 are similar (at least a score of thresh)
    def frame_same(self, img1, img2, thresh = 0.6):
        try:
            return ssim(img1, img2, multichannel = True) >= thresh
        except:
            print("error determining img similarity")
    
    # Take unique screenshots of the video (frame_same() is used to determine similarity)
    def take_screenies(self):
        vid = cv2.VideoCapture(self.path)
        
        count = 0
        prev_frame = 0
        while True:
            ret, frame = vid.read()
        
            if (prev_frame == 0) or (not self.frame_same(frame, prev_frame)):
                name = self.res_path + '/frame_{}.jpg'.format(str(count).zfill(2))
                print("Creating ", name)
                cv2.imwrite(name, frame)
                count += 1
            else:
                break
        vid.release()
        cv2.destroyAllWindows()
















































































































++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++