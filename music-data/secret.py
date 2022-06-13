import tekore as tk 

CLIENT_ID = '52793ece707444a59a7c4c52dbac71ad'
CLIENT_SECRET = '15e1a48beb114b9aa112b1cf74b32690'

def authorize():
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)