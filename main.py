from download import Video
from screenshot import Screenie
from combine import Join
import sys


'''
From a Youtube Video where video is sheet music, 
Take screenshots and join screenshots into sheet music
'''

def main(url, folder_name, file_name, trim = False):
    try:
        v = Video(url)
        video_file = file_name + '.mp4'
        v.download(video_file)
        
        s = Screenie(video_file, fname = folder_name)
        s.take_screenies()
        
        j = Join(folder_name, trim = trim)
        j.save(file_name + '.pdf')
        
    except:
        print("Error")

'''
if __name__ == '__main__':
    # main(sys.argv[1], sys.argv[2], sys.argv[3])
    print(sys.argv[1], sys.argv[2], sys.argv[3])
'''