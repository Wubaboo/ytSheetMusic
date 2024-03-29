# ytSheetMusic
(Here's a URL if you want to test it: https://www.youtube.com/watch?v=61Ln3Jy8WxU)

Get sheet music from youtube videos 
  - downloads, screenshots, crops, and combines sheet music elements
![ytSheetMusic](https://github.com/Wubaboo/ytSheetMusic/assets/59407231/05467c91-6bbb-4f25-a669-2e169cfc87d7)

**main.py**: 

  - Creates subsequent object classes and calls methods
  - *Usage*: main(url, file_name, thresholding = False, hands = False)
    - url (str): path to the Youtube Video
    - file_name (str): Name to save the downloaded video and the final pdf
    - hands (bool): if there are hands in the video (or non sheet music elements)
    
**download.py**:
  - Uses yt-dlp to download the video from the url
  
**screenshot.py**:
  - Take unique screenshots of frames and extract only the sheet music portions
  
**combine.py**: 
  - Concatenates screenshotted images to fit a page
  - Save as PDF

1. Get youtube video with sheet music in it

![youtube screenshot with sheet music](https://github.com/Wubaboo/ytSheetMusic/blob/main/img/YoutubeVideo.png?raw=true)

2. Run main.py`main(url, 'Clair de Lune', hands = True)` 

3. Check 'Sheet Music' folder in the directory for the resulting PDF
![resulting pdf](https://github.com/Wubaboo/ytSheetMusic/blob/main/img/res.png?raw=true)
