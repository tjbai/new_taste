# from rmn import RMN
import numpy as np
import pandas as pd
import cv2
import base64
import math
import os
from pathlib import Path
# from deepface import DeepFace

TEST_IMG = '../test-images/neutral.jpg'

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


# Deprecated in favor of the deepface solution
def detect_emotion_rmn(image):
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
    # Config DEEPFACE_HOME path
    # os.environ.setdefault("DEEPFACE_HOME", "./models")
    # Path('./models').mkdir(parents = True, exist_ok = True)
    # download_emotion_model()

    from deepface import DeepFace
    obj = DeepFace.analyze(img_path=image, actions=['emotion'])
    return obj['emotion']


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
def recommend(VA_score, n):
    df = pd.read_csv('../../music-data/VA_dataset.csv', encoding='utf-8')
    song_score = df[['valence', 'energy']].to_numpy() # Isolate valence and energy columns
    emo_score = np.tile(VA_score, (len(song_score), 1)) 

    # Vectorized euclidean distance between emo_score and song_score
    res = np.linalg.norm(emo_score - song_score, axis = 1)
    indices = np.arange(1, len(res))
    sorted_indices = sorted(indices, key = lambda x: res[x])

    # Pull out the top n from sorted_indices
    recommendations = []
    for index in sorted_indices[:n]:
        recommendations.append(df.iloc[index].to_list())

    return recommendations


if __name__ == '__main__':
    detect_emotion_deepface(TEST_IMG)


    



