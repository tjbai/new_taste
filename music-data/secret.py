import tekore as tk 
import csv

CLIENT_ID = 'made you look'
CLIENT_SECRET = 'nice try'

def authorize():
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)

def get_genres():
    sp = authorize()
    genres = sp.recommendation_genre_seeds()

    file = open('genres.csv', 'w')
    with file:
        write = csv.writer(file)
        write.writerow(genres)

if __name__ == '__main__':
    get_genres()