from flask import Flask, request, Response
from flask_cors import CORS
from main import main, customCombine, getBucketFiles
import json

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

'''
placeholder
'''
@app.get("/")
def hello_world():
    res = Response("<h1>ytSheetMusic</h1>")
    #res.headers.add('Access-Control-Allow-Origin','*') 
    #res.headers.add('Access-Control-Allow-Methods', '*')
    #res.headers.add('Access-Control-Allow-Headers', '*')
    return res


'''
body specifies 
{"threshold": "0.9", "hands": false, "url": "https://www.youtube.com/watch?v=pB_9AHiv2q0"}
'''
@app.post('/')
def post():
    data = request.get_json()
    print(data)
    threshold = 0.9
    hands = False
    if not 'url' in data:
        return "Include 'url' in body", 400
    if 'threshold' in data:
        threshold = float(data['threshold'])
    if 'hands' in data and data['hands']:
        hands = True
    try:
        print("calling main")
        res = Response(main(data['url'], hands = hands, threshold = threshold))
        # res.headers.add('Access-Control-Allow-Origin', '*')
        # res.headers.add('Access-Control-Allow-Methods', '*')
        # res.headers.add('Access-Control-Allow-Headers', '*')
        return res
    except:
        print('error')
        return "Error", 500

'''
body is a JSON with an array of frames
{"data": ["frame_000.jpg", "frame_001.jpg", "frame_003.jpg", "frame_004.jpg"]}
'''
@app.post('/<url>')
def combine(url):
    try:
        data = request.get_json()
        print('data', data, url)
        
        if 'data' in data:
            images_array = json.loads(data['data'])
            newFile = customCombine(url, images_array)
        else:
            return "Need 'data' field in body, with an array of frames", 400
        return json.dumps({'data': data, 'url': url, 'filename': newFile})
    except:
        return "Error", 500

'''
Get all the files relevant to the URL (screenshots and pdf if available)
'''
@app.get('/<url>')
def getImages(url):
    return json.dumps(getBucketFiles(url))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, ssl_context=("/etc/letsencrypt/live/ytsheetmusic.evanpai.com/fullchain.pem", "/etc/letsencrypt/live/ytsheetmusic.evanpai.com/privkey.pem"))    
    