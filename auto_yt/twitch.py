import requests
import yaml
import os
import json
import progressbar
import shutil

class Twitch:
    def __init__(self, client_id, client_secret, access_token):
        self.base_url = 'https://api.twitch.tv/helix/'
        self.oauth2_url = 'https://id.twitch.tv/oauth2/'
        self.root_path = os.getcwd()
        self.game = None
        self.clips = []
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token


    def get(self, url, payload, headers):
        response = requests.get(url, params=payload, headers=headers)
        if response.status_code == 401:
            data = json.loads(response.text)
            return data['message']
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


    def acquire_access_token(self) -> None:
        url = f'{self.oauth2_url}token'
        payload = { 'client_id':self.client_id, 'client_secret':self.client_secret, 'grant_type':'client_credentials' }
        data = self.post(url, payload, {})
        config_path = f'{self.root_path}/config.yaml'
        with open(config_path) as f:
            config_data = yaml.safe_load(f)    
        config_data['twitch']['access-token'] = data['access_token']
        self.access_token = data['access_token']
        with open('config.yaml', 'w') as f:
            yaml.safe_dump(config_data, f)
        print(f'Acquired access token: {self.access_token}')


    def check_token_valid(self) -> None:
        url = f'{self.oauth2_url}validate'
        headers = { 'Authorization' : f'Bearer {self.access_token}' }
        print(f'Checking validity of token: {self.access_token}')
        data = self.get(url, {}, headers)
        if data == 'invalid access token':
            print(data)
            self.acquire_access_token()
            return
        print('token is valid')


    def revoke_access_token(self) -> None:
        url = f'{self.oauth2_url}revoke'
        payload = { 'client_id':self.client_id, 'token':self.access_token }
        print(f'Revoking access token: {self.access_token}')
        data = self.post(url, payload, {})
        print(f'Successfully revoked access token: {self.access_token}')


    def download_clips(self) -> None:
        clips_url = f'{self.root_path}/auto_yt/clips'
        if not os.path.exists(clips_url):
            os.makedirs(clips_url)
        for clip in progressbar.progressbar(self.clips, prefix='Downloading clips: '):
            down_url = f'{clip["thumbnail_url"][0:-20]}.mp4'
            out_path = f'{clips_url}/{clip["id"]}.mp4'
            response = requests.get(down_url, stream=True)
            with open(out_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)         


    def get_clips(self, date, game_id: int, num_of_clips: int = 25, video_length: int = 600, clips_length: int = 0) -> None:
        url = f'{self.base_url}clips'
        headers = { 'Authorization' : f'Bearer {self.access_token}', 'Client-ID' : self.client_id }
        payload = { 'started_at': date, 'game_id': game_id, 'first': num_of_clips }
        data = self.get(url, payload, headers)
        for clip in data['data']:
            if clip['language'] != 'en':
                continue
            clips_length += clip['duration']
            self.clips.append(clip)
        if clips_length < video_length:
            self.get_clips(date, game_id, num_of_clips, clips_length)
