from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from PIL import Image
import io
import base64
from detect import *

app = Flask(__name__)
CORS(app)

INPUT_IMG = '../static/input.jpeg' 

# Test API Route
@app.route("/api", methods=['POST', 'GET'])
def api():
    # Process request and convert to image
    data = request.get_json()
    result = data['img'] # base64 encoded string


    b64 = bytes(result, 'utf-8') # bytes
    b64string = b64[b64.find(b'/9'):] # pulling out the string portion
    im = Image.open(io.BytesIO(base64.b64decode(b64string))) # open with Pillow
    im.save(INPUT_IMG) # save to local

    # Face => emotions
    face_res = detect_faces(INPUT_IMG) 
    emotion_list = detect_emotion_deepface(INPUT_IMG) 

    # Emotions => recommendations
    emotion_score = to_VA_score(emotion_list)
    recos = recommend(emotion_score, data['songCount'])

    return jsonify({
        'count': face_res[0],
        'img': face_res[1], 
        'emotions': emotion_list,
        'songs': recos
    })

if __name__ == '__main__':
    app.run()
