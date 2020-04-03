import yaml
from auto_yt.platforms.twitch import Twitch

with open('config.yaml') as f:
    data = yaml.safe_load(f)
    print(data)

twitch_config = data['twitch']
twitch = Twitch(twitch_config['client-id'], twitch_config['client-secret'], twitch_config['access-token'])
twitch.test()