from download import Video
from screenshot import Screenie
from combine import Join
import sys
import os
from awsServices import bucket, getFiles, downloadFile, deleteFile
import json
import shutil
from datetime import datetime
import gc
import time


'''
From a Youtube Video where video is sheet music, 
Take screenshots and join screenshots into sheet music
- Need FFMPEG in the PATH (Or in the directory)
- Need yt-dlp in the PATH (Or in the directory)

'''


# url: path to the Youtube Video
# file_name: Name to save the downloaded video and the final pdf
# hands: if there are hands in the picture (or non sheet music elements)
def main(url, file_name=None, hands = False, threshold=0.9):
    if not file_name:
        base_url, delimiter, file_name = url.rpartition('watch?v=')
        
    allFiles = getFiles(bucket)
    if file_name in allFiles and threshold == 0.9 and f"{file_name}.pdf" in allFiles[file_name]:
        return json.dumps({'filename': file_name})
    
    folder_name = ''.join(file_name.split(' '))
    try:
        if file_name + '.mp4' not in os.listdir():
            v = Video(url)
            v.download(file_name, form = 'mp4')
            del v
        print('Taking Screenie')
        s = Screenie(file_name +'.mp4', fname = folder_name, hands = hands, threshold=threshold)
        s.take_screenies()
        print('Uploading Images')
        s.upload_images()
        del s
        gc.collect()
        deleteFile(f'{url}/{url}.pdf')
        j = Join(folder_name)      
        j.save(file_name + '.pdf')
        j.upload_file(file_name +'.pdf')
        del j
        gc.collect()
        cleanup(file_name)
        return json.dumps({'filename': file_name})
        
    except:
        print("Error")
        return None

def cleanup(filename):
    if f'{filename}.mp4' in os.listdir():
        os.remove(f'{filename}.mp4')
    if f'{filename}' in os.listdir():
        shutil.rmtree(f'{filename}')
    
# Given the url path and an array of frames, combine the images and save a pdf
def customCombine(filename, files):
    for f in files:
        fullName=f"{filename}/{f}"
        downloadFile(fullName, fullName, bucket)
        print(f'downloaded {fullName}')
    
    timeStr = str(datetime.now()).replace('.', '-').replace(':', '-').replace(' ', '-')
    newFile = f"{filename}_{timeStr}.pdf"
    j = Join(filename)
    j.save(newFile)
    j.upload_file(newFile)
    cleanup(filename)
    return newFile

def getBucketFiles(filename):
    allFiles = getFiles(bucket, prefix=filename)
    return allFiles
    

    
    
