'''
From a Youtube Video where video is sheet music, 
Take screenshots and join screenshots into sheet music
'''

import pafy

## Given a URL, download the video, or audo, or both

## url = 'https://www.youtube.com/watch?v=-qPark5JTOo'
## v = Video(url)
## v.download('All I want for Christmas')
class Video():
    def __init__(self, url):
        self.url = url
        self.video = pafy.new(url)
        #self.title = 
    
    def download(self, filename = '', audio = True, video = True):
        if audio and video:
            self.video.getbest().download(filename)
        elif audio:
            self.video.getbestaudio(preftype = 'mp3').download(filename)
        elif video:
            self.video.getbestvideo(preftype = 'mp4').download(filename)
