import numpy as np
import pandas as pd
import cv2
import base64
import math
import os
from pathlib import Path
import pprint
# from deepface import DeepFace

TEST_IMG = '../test-images/jehan-happy.jpg'

CONFIG = './models/deploy.prototxt.txt'
MODEL = './models/res10_300x300_ssd_iter_140000.caffemodel'
CONFIDENCE_LEVEL = 0.5


def test():
    return 'I MADE IT'


def detect_faces(image):
    # Load model
    net = cv2.dnn.readNetFromCaffe(CONFIG, MODEL)
    img = cv2.imread(image)
    h, w = img.shape[:2]

    # Mean subtraction and channel swapping
    blob = cv2.dnn.blobFromImage(cv2.resize(
        img, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))

    net.setInput(blob)
    faces = net.forward()  # Detect faces

    # Find faces and draw a box around them
    ct = 0
    for i in range(faces.shape[2]):
        confidence = faces[0, 0, i, 2]
        if confidence > CONFIDENCE_LEVEL:
            ct = ct+1
            box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype('int')
            cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 2)

    # Encode img to b64 again
    __, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    res = jpg_as_text.decode('utf-8')

    return [ct, res]


def detect_with_haar(image):
    # Load cascade
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Process the image
    img = cv2.imread(IMG)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 7)

    ct = 0
    for (x, y, w, h) in faces:
        ct = ct+1
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return ct


# deprecated...
def detect_emotion_rmn(image):
    from rmn import RMN

    m = RMN()
    image = cv2.imread(image)
    results = m.detect_emotion_for_single_frame(image)
    return results[0]['proba_list']


def download_emotion_model():
    # Install model weights to correct location
    model_url = "https://github.com/serengil/deepface_models/releases/download/v1.0/facial_expression_model_weights.h5"
    os.system(
        f"wget {model_url} -O ./models/facial_expression_model_weights.h5"
    )

def detect_emotion_deepface(image):
    # os.environ.setdefault("DEEPFACE_HOME", "./models")
    # Path('./models').mkdir(parents = True, exist_ok = True)
    # download_emotion_model()

    from deepface import DeepFace

    obj = DeepFace.analyze(img_path=image, actions=['emotion'])
    return obj['emotion']


# deprecated...
def detect_emotion_fer(image):
    from fer import FER
    from fer.utils import draw_annotations

    img = cv2.imread(image)
    detector=FER()

    res = detector.detect_emotions(img)
    img = draw_annotations(img, res)

    print(res)


hsq2 = math.sqrt(2)/2
DIRS = { # Direction array for all 7 detected emotions
    'angry': np.array([-.5,.5]),
    'disgust': np.array([-hsq2,0]),
    'fear': np.array([-hsq2,0]),
    'happy': np.array([.5,-.5]),
    'sad': np.array([-.5,-.5]),
    'surprise': np.array([.5,.5]),
    'neutral': np.array([0,0])
}

# Converts emotion list into 2D valence-arousal vector
def to_VA_score(emo_list):
    score = np.array([0.5,0.5])
    for emotion in DIRS.keys():
        score = score + emo_list[emotion] / 100 * DIRS[emotion]
    return score


# Look for n-closest songs in R^2 by euclidean distance
def recommend(VA_score, n, genre_filter):
    # Create dataframe 
    df = pd.read_csv('../../music-data/VA_dataset.csv', encoding='utf-8')

    # If genre_filter is non-trivial, filter
    if len(genre_filter) > 0:
        genres = []
        for g in genre_filter:
            genres.append(g['label'])
        df.query('genre in @genres', inplace = True)

    # Isolate song and emotion matrices
    song_score = df[['valence', 'energy']].to_numpy() 
    emo_score = np.tile(VA_score, (len(song_score), 1)) 

    # Vectorized euclidean distance 
    res = np.linalg.norm(emo_score - song_score, axis = 1)
    indices = np.arange(1, len(res))
    sorted_indices = sorted(indices, key = lambda x: res[x])

    # Pull out the top n from sorted_indices
    recommendations = []
    for index in sorted_indices[:n]:
        recommendations.append(df.iloc[index].to_list())

    return recommendations


if __name__ == '__main__':
    values = ['happy', 'heavy-metal', 'r-n-b']
    score = np.array([1,1])
    n = 3;
    recos = recommend(score, n, values)

    print(recos)


    



