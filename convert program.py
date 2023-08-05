import moviepy.editor as moviepy
from PIL import Image
import cv2

def get_video_aspect_ratio(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    aspect_ratio = frame_width / frame_height
    return aspect_ratio

def convert_video(file_name: str, new_ext: str):
    split_file_name = file_name.rsplit('.')
    try:
        clip = moviepy.VideoFileClip(file_name)
        clip.write_videofile(split_file_name[0] + new_ext)
    except Exception as e:
        print('Error occurred during conversion: ' + e)

    
def convert_image(file_name: str, new_ext: str):
    try:
        img = Image.open(file_name)
        img.save(file_name, new_ext.lstrip('.'))
    except IOError as e:
        print('Error occurred; the sent file might not exist: ' + e)
    except Exception as e:
        print('Error occurred during conversion: ' + e)

def main():
    while True:
        choice = input('Do you want to convert images, or video? Enter in i and v respectively: ')
        if choice.lower() == 'i':
            image_path = input('Enter the path of the image to convert: ')
            new_ext = input('Enter the new type of the image will be, like this: .exe ')
            if not(new_ext.startswith('.')):
                print('Try again.')
                continue

            convert_image(image_path, new_ext)

        elif choice.lower() == 'v':
            video_path = input('Enter the path of the video to convert: ')
            new_ext = input('Enter the new type of the video will be, like this: .exe ')
            if not(new_ext.startswith('.')):
                print('Try again.')
                continue
            
            convert_video(video_path, new_ext)

        else:
            print('Try again.')

main()

