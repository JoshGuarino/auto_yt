from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

class Edit:
    def __init__(self):
        self.clip_dir = f'{os.getcwd()}/auto_yt/clips'

    def concat_clips(self, sub_dir):
        clip_list = []
        for file in os.listdir(self.clip_dir):
            clip_list.append(VideoFileClip(f'{self.clip_dir}/{sub_dir}/{file}'))
        return concatenate_videoclips(clip_list)


    def write_final_video(self, final_clip, write_dir):
        final_clip.write_videofile(write_dir)