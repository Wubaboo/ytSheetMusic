from flask import Flask, request, Response
from flask_cors import CORS
from main import main, customCombine, getBucketFiles
import json
from waitress import serve

app = Flask(__name__)
CORS(app)

'''
placeholder
'''
@app.get("/")
def hello_world():
    res = Response("<h1>ytSheetMusic</h1>")
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


'''
body specifies 
{"threshold": "0.9", "hands": false, "url": "https://www.youtube.com/watch?v=pB_9AHiv2q0"}
'''
@app.post('/')
def post():
    data = request.get_json()

    threshold = 0.9
    hands = False
    if not 'url' in data:
        return "Include 'url' in body", 400
    if 'threshold' in data:
        threshold = float(data['threshold'])
    if 'hands' in data and data['hands']:
        hands = True
    try:
        # res = Response(main(data['url'], hands = hands, threshold = threshold))
        # res.headers.add('Access-Control-Allow-Origin', '*')
        # res.headers.add('Access-Control-Allow-Methods', '*')
        # res.headers.add('Access-Control-Allow-Headers', '*')
        return main(data['url'], hands = hands, threshold = threshold)
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
        print('data', url)
        if 'data' in data:
            customCombine(url, data['data'])
        else:
            return "Need 'data' field in body, with an array of frames", 400
        return json.dumps({'data': data, 'url': url})
    except:
        return "Error", 500

'''
Get all the files relevant to the URL (screenshots and pdf if available)
'''
@app.get('/<url>')
def getImages(url):
    return json.dumps(getBucketFiles(url))
    
    

# if __name__ == '__main__':
#     serve(app, host='0.0.0.0', port=8080)