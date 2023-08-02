import moviepy.editor as moviepy

def convert_video(file_name: str, new_ext: str):
    split_file_name = file_name.rsplit('.')
    clip = moviepy.VideoFileClip(file_name)
    clip.write_videofile(split_file_name[0] + new_ext)
    