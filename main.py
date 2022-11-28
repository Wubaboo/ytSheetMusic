from download import Video
from screenshot import Screenie
from combine import Join
import sys
import os

'''
From a Youtube Video where video is sheet music, 
Take screenshots and join screenshots into sheet music
- Need FFMPEG in the PATH (Or in the directory)
- Need yt-dlp in the PATH (Or in the directory)

'''


# url: path to the Youtube Video
# file_name: Name to save the downloaded video and the final pdf
# trim : If there is a border around the sheet music, it can be cropped out
# hands: if there are hands in the picture (or non sheet music elements)
def main(url, file_name, trim = True, thresholding = False, hands = False):
    folder_name = ''.join(file_name.split(' '))
    try:
        if file_name + '.mp4' not in os.listdir():
            v = Video(url)
            v.download(file_name, form = 'mp4')
            
        s = Screenie(file_name +'.mp4', fname = folder_name, thresholding = thresholding, hands = hands)
        s.take_screenies()
        
        j = Join(folder_name)
        j.save(file_name + '.pdf')
        
    except:
        print("Error")

