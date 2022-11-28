#import pafy
#from pydub import AudioSegment
import os


''' THIS SHOULD NOT USE PAFY. PAFY IS SLOW. USE yt-dlp'''

'''
 Given a URL, download the video, or audo, or both

## url = 'https://www.youtube.com/watch?v=-qPark5JTOo'
## v = Video(url)
## v.download('All I want for Christmas')
'''

'''OBSOLETE
class Video():
    def __init__(self, url):
        self.url = url
        self.video = pafy.new(url)
    
    def convert(self, fname, dest):
        downloaded = AudioSegment.from_file(fname, fname.split('.')[-1])
        downloaded.export(dest, format='mp3')
        
    ## Download the youtube video from self.url saving it with the
    ## given filename
    def download(self, filename = '', audio = True, video = True):
        if audio and video:
            self.video.getbest().download(filename)
        elif audio:
            aud_fname = self.video.getbestaudio().download()
            self.convert(aud_fname, f'downloads/{filename}.mp3')
'''

class Video():
    def __init__(self, url):
        self.url = url
        
    def download(self, fname = '', form = 'mp4'):
        if fname:
            os.system(f'yt-dlp --format {form} -o "{fname}.{form}" {self.url}')
        else:
            os.system(f'yt-dlp --format {form} {self.url}')
