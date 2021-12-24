import pafy

'''
 Given a URL, download the video, or audo, or both

## url = 'https://www.youtube.com/watch?v=-qPark5JTOo'
## v = Video(url)
## v.download('All I want for Christmas')
'''
class Video():
    def __init__(self, url):
        self.url = url
        self.video = pafy.new(url)
        
    ## Download the youtube video from self.url saving it with the
    ## given filename
    def download(self, filename = '', audio = True, video = True):
        if audio and video:
            self.video.getbest().download(filename)
        elif audio:
            self.video.getbestaudio(preftype = 'mp3').download(filename)
        elif video:
            self.video.getbestvideo(preftype = 'mp4').download(filename)
