'''
From a Youtube Video where video is sheet music, 
Take screenshots and join screenshots into sheet music
'''


import pafy

## Given a URL, download the video, or audo, or both
class Video():
    def __init__(self, url):
        self.url = url
        self.video = pafy.new(url)
        
    
    def download(self, path = '', audio = True, video = True):
        if audio and video:
            self.video.getbest().download(path)
        if audio:
            self.video.getbestaudio().download(path)
        if video:
            self.video.getbestvideo().download(path)
