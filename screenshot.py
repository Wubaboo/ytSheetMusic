import cv2 
import os
from skimage.metrics import structural_similarity as ssim

'''
Take unique screenshots of every 100 frames

'''
class Screenie():
    def __init__(self, vid_path, fname = 'screenies'):
        self.path = vid_path
        
        self.res_path = self.make_folder(fname)
    
    # Make a new folder "fname"
    def make_folder(self, name = 'screenies'):
        try:
            if not os.path.exists(name):
                os.makedirs(name)
            return name
        except:
            return 'screenies'
            
    
    # Determines if img1 and img2 are similar (at least a score of thresh)
    def frame_same(self, img1, img2, thresh = 0.8):
        try:
            return ssim(img1, img2, multichannel = True) >= thresh
        except:
            print("error determining img similarity")
    
    # Take unique screenshots of the video (frame_same() is used to determine similarity)
    def take_screenies(self, interval = 100):
        vid = cv2.VideoCapture(self.path)
        
        count = 0
        name_count = 0 
        prev_frame = 0
        while True:
            ret, frame = vid.read()
            if not ret: break
            if count % interval == 0:
                if (isinstance(prev_frame, int)) or (not self.frame_same(frame, prev_frame)):
                    name = self.res_path + '/frame_{}.jpg'.format(str(name_count).zfill(2))
                    print("Creating ", name)
                    print(count)
                    cv2.imwrite(name, frame)
                    prev_frame = frame
                    name_count += 1
            count += 1
            
        vid.release()
        cv2.destroyAllWindows()
