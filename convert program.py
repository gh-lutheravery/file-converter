import moviepy.editor as moviepy

def convert_video(file_name: str, new_ext: str):
    split_file_name = file_name.rsplit('.')
    clip = moviepy.VideoFileClip(file_name)
    clip.write_videofile(split_file_name[0] + new_ext)

def main():
    choice = input('Do you want to convert images, or video? Enter in i and v respectively: ')
    if choice.lower() == 'i':
        image_path = input('Enter the path of the image to convert: ')
        new_ext = input('Enter the new type of the image will be, like this: .exe ')
        convert_image(image_path, new_ext)
        
    elif choice.lower() == 'v':
        video_path = input('Enter the path of the video to convert: ')
        new_ext = input('Enter the new type of the video will be, like this: .exe ')
        convert_video(video_path, new_ext)

