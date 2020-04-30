import yaml
from auto_yt.platforms.twitch import Twitch

def main():

    with open('config.yaml') as f:
        data = yaml.safe_load(f)

    twitch_config = data['twitch']
    twitch = Twitch(twitch_config['client-id'], twitch_config['client-secret'], twitch_config['access-token'])
    twitch.check_token_valid()
    twitch.clips = twitch.get_clips('2020-03-30T00:00:00Z', 32982, 1)
    twitch.download_clips()
    twitch.revoke_access_token()

if __name__ == "__main__":
    main()