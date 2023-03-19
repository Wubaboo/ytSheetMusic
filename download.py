import os

'''
 Given a URL, download the video, or audo, or both

## url = 'https://www.youtube.com/watch?v=-qPark5JTOo'
## v = Video(url)
## v.download('All I want for Christmas')
'''

class Video():
    def __init__(self, url):
        self.url = url
        
    def download(self, fname = '', form = 'mp4'):
        if fname:
            os.system(f'yt-dlp --format {form} -o "{fname}.{form}" {self.url}')
        else:
            os.system(f'yt-dlp --format {form} {self.url}')
