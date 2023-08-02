import moviepy.editor as moviepy

def convert_video(file_name: str):
    split_file_name = file_name.rsplit('.')
    clip = moviepy.VideoFileClip(file_name)