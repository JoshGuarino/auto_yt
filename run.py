import yaml
from auto_yt.twitch import Twitch
from auto_yt.edit import Edit
from auto_yt.youtube import Youtube
import datetime

def main() -> None:
    with open('config.yaml') as f:
        data = yaml.safe_load(f)
    date = datetime.date.today() - datetime.timedelta(days=7)

    # set configs
    twitch_config = data['twitch']
    youtube_config = data['youtube']
    
    # create twitch object, download and get clips 
    twitch = Twitch(twitch_config['client-id'], twitch_config['client-secret'], twitch_config['access-token'])
    twitch.check_token_valid()
    for game in twitch_config['games']:
        twitch.get_clips(f'{date}T00:00:00Z', game, 100)
    twitch.download_clips()
    twitch.revoke_access_token()

    # create edit object and make final video
    edit = Edit()
    final_clip = edit.concat_clips()
    edit.write_final_video(final_clip, '/')
    edit.cleanup_clips_dir()

    # create youtube object and upload to channel
    youtube = Youtube(youtube_config['access-token'])
    youtube.upload_video()

if __name__ == "__main__":
    main()
