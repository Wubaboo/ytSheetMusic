from download import Video
from screenshot import Screenie
from combine import Join
import sys
import os

'''
From a Youtube Video where video is sheet music, 
Take screenshots and join screenshots into sheet music
'''

def main(url, folder_name, file_name, trim = False, thresholding = False):
    try:
        video_file = file_name + '.mp4'
        if video_file not in os.listdir():
            v = Video(url)
            v.download(video_file)
            
        s = Screenie(video_file, fname = folder_name, thresholding = thresholding)
        s.take_screenies()
        
        j = Join(folder_name, trim = trim)
        j.save(file_name + '.pdf')
        
    except:
        print("Error")

'''
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    #print(sys.argv[1], sys.argv[2], sys.argv[3])
'''