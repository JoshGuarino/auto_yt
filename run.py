import yaml
from auto_yt.twitch import Twitch
from auto_yt.edit import Edit
from auto_yt.youtube import Youtube
import datetime

def main() -> None:
    with open('config.yaml') as f:
        data = yaml.safe_load(f)
    date = datetime.date.today() - datetime.timedelta(days=7)
    twitch_config = data['twitch']
    twitch = Twitch(twitch_config['client-id'], twitch_config['client-secret'], twitch_config['access-token'])
    twitch.check_token_valid()
    for game in twitch_config['games']:
        twitch.get_clips(f'{date}T00:00:00Z', game, 100)
    twitch.download_clips()
    twitch.revoke_access_token()

if __name__ == "__main__":
    main()
