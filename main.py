from download import Video
from screenshot import Screenie
from combine import Join
import sys
import os

'''
From a Youtube Video where video is sheet music, 
Take screenshots and join screenshots into sheet music

TO DO:
    - In Screenshot.py, use relative area of the bounded rectangle to determine sheet 
    music regions?
'''

# url: path to the Youtube Video
# folder_name: is the name to label the folder containing all the screenshots
# file_name: Name to save the downloaded video and the final pdf
# trim : If there is a border around the sheet music, it can be cropped out
# 
def main(url, folder_name, file_name, trim = True, thresholding = False, hands = False):
    try:
        video_file = file_name + '.mp4'
        if video_file not in os.listdir():
            v = Video(url)
            v.download(video_file)
            
        s = Screenie(video_file, fname = folder_name, thresholding = thresholding, hands = hands)
        s.take_screenies()
        
        j = Join(folder_name)
        j.save(file_name + '.pdf')
        
    except:
        print("Error")

'''
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    #print(sys.argv[1], sys.argv[2], sys.argv[3])
'''