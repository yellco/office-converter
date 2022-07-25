from moviepy.editor import VideoFileClip


def convert(video_file):
    videoClip = VideoFileClip("my-life.mp4")
    videoClip.write_gif("my-life.gif")
