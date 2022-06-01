import os
import json 
import cv2 
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import numpy as np
import json 
import argparse


class VideoMaker:

    def __init__(self, im_dir, metadata_dir, audio_dir, out_dir, fps, map_file):
        self.mapping = self.load_json(map_file)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        self.height, self.width = self.get_im_dims(im_dir)
        self.im_dir = im_dir
        self.metadata_dir = metadata_dir
        self.audio_dir = audio_dir
        self.out_dir = out_dir
        self.fps = fps

    def load_json(self, f):
        with open(f, 'r') as o:
            return json.load(o)

    def get_im_dims(self, im_dir): # should first check the file is an image
        for image in os.listdir(im_dir):
            try:
                frame = cv2.imread(os.path.join(im_dir, image))
                height, width, channels = frame.shape
                return height, width
            except:
                continue

    def get_out(self, out_path):
        return cv2.VideoWriter(out_path, self.fourcc, self.fps, (self.width, self.height))

    def read_chunk_data(self, chunk):
        return self.mapping[chunk['viseme']], chunk['duration']

    def make_frame(self, viseme):
        frame = cv2.imread(os.path.join(self.im_dir, f"{viseme}.jpeg")) # allow other file types
        return cv2.resize(frame, (self.width, self.height))

    def frame_to_video(self, output, frame, dur):
        for i in range(int(np.round(dur/1000*self.fps, 0))):
            output.write(frame) 

    def generate_video(self, in_file):
        in_path = os.path.join(self.metadata_dir, in_file)
        self.out_path = (os.path.join(self.out_dir, f'{in_file.strip(".json")}_{self.fps}.mp4'))
        output = self.get_out(self.out_path)
        data = self.load_json(in_path)['phonemes']
        viseme_dur = 0
        for chunk in data:
            mapped, dur = self.read_chunk_data(chunk)
            frame = self.make_frame(mapped)
            self.frame_to_video(output, frame, dur)
            viseme_dur += dur
        output.release()
        cv2.destroyAllWindows()
        print(f"Generated video of {viseme_dur} milliseconds from viseme images.")

    def add_audio(self, audio_file, video_file):
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)
        print(f"Adding audio stream of {audio_clip.end} milliseconds.")
        if video_clip.end < audio_clip.end:
            audio_clip = audio_clip.subclip(0, video_clip.end)
            print(f"Clipped audio file to {video_clip.end} milliseconds.")
        elif audio_clip.end < video_clip.end:
            video_clip = video_clip.subclip(0, audio_clip.end)
            print(f"Clipped video file to {audio_clip.end} milliseconds.")

        final_video = video_clip.set_audio(audio_clip)
        print(f"Successfully generated video of {final_video.end} milliseconds from video and audio streams.")
        video_out_path = f'video/{os.path.basename(self.im_dir)}_with_audio_{video_file.strip(".json").strip("video/")}'
        final_video.write_videofile(video_out_path, fps=self.fps)
        print(f"Video successfully saved to {video_out_path}.")


def main():
    parser = argparse.ArgumentParser(description='Specify metadata, audio, image and output directories, and viseme mapping file.')
    parser.add_argument("--im_dir",  type=str, default='image/mouth1', help='Directory with viseme images.')
    parser.add_argument("--metadata_dir",  type=str, default='metadata', help='Directory containing viseme metadata .json files.')
    parser.add_argument("--audio_dir",  type=str, default='audio', help='Directory containing .wav audio files.')
    parser.add_argument("--out_dir", type=str, default='video', help='Directory to save generated video.')
    parser.add_argument("--fps", type=int, default=20, help='Frame rate (in frames per second) to generate video.')
    parser.add_argument("--map", type=str, default='map/viseme_map.json', help='Path to viseme mapping file.')
    parser.add_argument("--no_audio", action='store_true', help='Generated video without audio.')
    args = parser.parse_args()
    viseme_video_maker = VideoMaker(args.im_dir, args.metadata_dir, args.audio_dir,  args.out_dir, args.fps, args.map)

    for in_file in os.listdir(args.metadata_dir):
        if '.json' not in in_file:
            continue
        else:
            viseme_video_maker.generate_video(in_file)
            if args.no_audio is not True:
                viseme_video_maker.add_audio(f'audio/{in_file.strip(".json")}.wav', viseme_video_maker.out_path)
                

if __name__ == "__main__":
    main()