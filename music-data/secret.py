import tekore as tk 

CLIENT_ID = 'nice try'
CLIENT_SECRET = 'made you look'

def authorize():
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)