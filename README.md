# ytSheetMusic
Get sheet music from youtube videos 
  - downloads, screenshots, crops, and combines sheet music elements

*main.py*: 
  - Creates subsequent object classes and calls methods
  - *Usage*: main(url, file_name, thresholding = False, hands = False)
    - url (str): path to the Youtube Video
    - file_name (str): Name to save the downloaded video and the final pdf
    - hands (bool): if there are hands in the video (or non sheet music elements)
    
*download.py*:
  - Uses yt-dlp to download the video from the url
  
*screenshot.py*:
  - Take unique screenshots of frames and extract only the sheet music portions
  
*combine.py*: 
  - Concatenates screenshotted images to fit a page
  - Save as PDF
  
 

