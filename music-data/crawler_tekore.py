import pandas as pd 
from tqdm import tqdm
import time
import secret

# Authorize and get tekore object
sp = secret.authorize()

genres = sp.recommendation_genre_seeds()
# time.sleep(10)  
n_recs = 100

data_dict = {'id': [], 'genre': [], 'track_name': [], 
            'artist_name': [], 'valence': [], 'energy': []}

"""
CRAWL DATA FROM SPOTIFY WEB API
"""
for g in tqdm(genres):
    recs = sp.recommendations(genres=[g], limit=n_recs) # Grab recs
    recs = eval(recs.json() # Some minor data cleaning
        .replace('null', '-999')
        .replace('false', 'False')
        .replace('true', 'True'))['tracks']

    # Crawl data from each track
    for track in recs:
        try:
            # ID and Genre
            data_dict["id"].append(track["id"])
            data_dict["genre"].append(g)
            # Metadata
            track_meta = sp.track(track["id"])
            data_dict["track_name"].append(track_meta.name)
            data_dict["artist_name"].append(track_meta.album.artists[0].name)
            # Valence and energy
            track_features = sp.track_audio_features(track["id"])
            data_dict["valence"].append(track_features.valence)
            data_dict["energy"].append(track_features.energy)

            time.sleep(0.2)
        except:
            print("Encountered an error, continuing for now")

"""
SLAM THE DATA IN A .CSV
"""
df = pd.DataFrame(data_dict)
df.drop_duplicates(subset='id', keep='first', inplace=True)
df.to_csv('VA_dataset.csv', index=False)

