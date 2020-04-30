import requests
import yaml
import os
import json
import progressbar
import shutil

class Twitch:
    def __init__(self, client_id, client_secret, access_token):
        self.main_path = 'https://api.twitch.tv/helix/'
        self.oauth2_path = 'https://id.twitch.tv/oauth2/'
        self.root_path = os.getcwd()
        self.game = None
        self.clips = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token


    def get(self, url, payload, headers):
        response = requests.get(url, params=payload, headers=headers)
        if response.status_code == 401:
            data = json.loads(response.text)
            self.acquire_access_token()
            return data
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        print(response.text)
        exit(1)


    def post(self, url, payload, headers):
        response = requests.post(url, params=payload, headers=headers)
        if response.status_code == 200:
            if response.text == '':
                return
            data = json.loads(response.text)
            return data
        print(response.text)
        exit(1) 


    def acquire_access_token(self):
        url = '{}token'.format(self.oauth2_path)
        payload = { 'client_id':self.client_id, 'client_secret':self.client_secret, 'grant_type':'client_credentials' }
        data = self.post(url, payload, {})
        config_path = '{}/config.yaml'.format(self.root_path)
        with open(config_path) as f:
            config_data = yaml.safe_load(f)    
        config_data['twitch']['access-token'] = data['access_token']
        self.access_token = data['access_token']
        with open('config.yaml', 'w') as f:
            yaml.safe_dump(config_data, f)
        print('Acquired access token: {}'.format(data['access_token']))
        return


    def check_token_valid(self):
        url = '{}validate'.format(self.oauth2_path)
        headers = { 'Authorization' : 'OAuth {}'.format(self.access_token) }
        print('Checking validity of token: {}'.format(self.access_token))
        data = self.get(url, {}, headers)
        print('Token is valid.')
        return


    def revoke_access_token(self):
        url = '{}revoke'.format(self.oauth2_path)
        payload = { 'client_id':self.client_id, 'token':self.access_token }
        print('Revoking access token: {}'.format(self.access_token))
        data = self.post(url, payload, {})
        print('Successfully revoked access token: {}'.format(self.access_token))
        return


    def download_clips(self):
        clips_url = f'{self.root_path}/auto_yt/clips/'
        if not os.path.exists(clips_url):
            os.makedirs(clips_url)
        for clip in progressbar.progressbar(self.clips, prefix='Downloading clips: '):
            url = '{}.mp4'.format(clip['thumbnail_url'][0:-20])
            out_path = '{}/auto_yt/clips/{}'.format(self.root_path, clip['video_id'])
            response = requests.get(url, stream=True)
            with open(out_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)         
        return


    def get_clips(self, date, game_id, num_of_clips):
        url = '{}clips'.format(self.main_path)
        headers = { 'Authorization' : 'OAuth {}'.format(self.access_token), 'Client-ID' : self.client_id }
        payload = { 'started_at':date, 'game_id': game_id, 'first':num_of_clips }
        data = self.get(url, payload, headers)
        return data['data']