import moviepy.editor as moviepy
from PIL import Image
import cv2
import os

def print_title():
    print('\n')
    print('Python Image and Video Converter')
    print(' Supported formats:')
    print(' Images: PNG, JPG, TIFF, WEBP, BMP')
    print(' Videos: MKV, MP4\n')

def convert_mkv_mp4(file_name: str, new_ext: str):
    split_file_name = file_name.rsplit('.')
    try:
        clip = moviepy.VideoFileClip(file_name)
        clip.write_videofile(split_file_name[0] + new_ext)
    except Exception as e:
        print('Error occurred during conversion: ' + str(e))

    
def convert_image(file_name: str, new_ext: str):
    try:
        split_file_name = file_name.rsplit('.')
        img = Image.open(file_name)

        print('Beginning conversion...')
        rgb_img = img.convert('RGB')
        rgb_img.save(split_file_name[0] + new_ext)
        print('Conversion finished.')
    except FileNotFoundError as e:
        print('Error occurred; the sent file might not exist: ' + str(e))
    except Exception as e:
        print('Error occurred during conversion: ' + str(e))


def main():
    while True:
        print_title()
        supported_imgs = ['PNG', 'JPG', 'TIFF', 'WEBP', 'BMP']
        supported_vids = ['MKV', 'MP4']

        choice = input('Do you want to convert images, or video? Enter in i and v respectively, or press q to quit: ')
        if choice.lower() == 'i':
            image_path = input('Enter the path of the image to convert: ')
            if not(os.path.exists(image_path) and os.path.isfile(image_path)):
                img_ext = image_path.rsplit('.')[1].upper()
                if not(img_ext in supported_imgs):
                    print('That file is not supported, try again.')
                    continue
                
                print('That image path does not seem to exist, try again.')
                continue

            new_ext = input('Enter the new type of the image will be, like this: .exe ')
            new_ext_stripped = new_ext.lstrip('.').upper()
            if not(new_ext_stripped in supported_imgs):
                print('Try again.')
                continue

            convert_image(image_path, new_ext)

        elif choice.lower() == 'v':
            video_path = input('Enter the path of the video to convert: ')
            if not(os.path.exists(video_path) and os.path.isfile(video_path)):
                vid_ext = video_path.rsplit('.')[1].upper()
                if not(vid_ext in supported_vids):
                    print('That file is not supported, try again.')
                    continue

                print('That video path does not seem to exist, try again.')
                continue

            new_ext = input('Enter the new type of the video will be, like this: .exe ')
            new_ext_stripped = new_ext.lstrip('.').upper()
            if new_ext_stripped in supported_vids:
                print('Try again.')
                continue
            
            convert_mkv_mp4(video_path, new_ext)

        elif choice.lower() == 'q':
            break

        else:
            print('Try again.')

main()

