import requests
import yaml

class Twitch:
    def __init__(self, client_id, client_secret, access_token):
        self.base_path = 'https://api.twitch.tv/helix/'
        self.game = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

    def get_access_token():
        return

    def check_token_valid(): 
        return

    def revoke_access_token():
        return

    def get_game():
        return

    def get_clips():
        return

    def test(self):
        print(self.client_id, self.client_secret, self.access_token)