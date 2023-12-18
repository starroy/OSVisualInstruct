import cv2
import os

import os


def convert_video_to_images(video_path, output_folder):
    # Read the video
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        # print("not exists")
        

    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    count = 0

    # Iterate through the video frames
    while success:
        # Save frame as an image
        image_path = f"{output_folder}/frame_{count}.jpg"
        cv2.imwrite(image_path, frame)
        
        # Read the next frame
        success, frame = video.read()
        count += 1

    # Release the video capture object
    video.release()


# Get the path to the directory
directory_path = "E:\\New folder\\win10"
out_path = "E:\\New folder\\win10_pic"


def read_sub_files(directory_path):
    files_and_subdirectories = os.listdir(directory_path)

    for file_or_subdirectory in files_and_subdirectories:
        if os.path.isfile(os.path.join(directory_path, file_or_subdirectory)):
            video_path = os.path.join(directory_path, file_or_subdirectory)
            output_path = os.path.join(out_path, file_or_subdirectory)[0:-4]
            print("current : ", output_path)
            convert_video_to_images(video_path, output_path)
        # If the file or subdirectory is a subdirectory, recursively read its subfiles
        elif os.path.isdir(os.path.join(directory_path, file_or_subdirectory)):
            read_sub_files(os.path.join(directory_path, file_or_subdirectory))

read_sub_files(directory_path)


# # Specify the path to the input video and the output folder
# video_path = "C:\\Users\\WhiteHorse\\Downloads\\win10\\1920x1080\\7zfm\\7zFM_activewindow.mp4"
# output_folder = "C:\\Users\\WhiteHorse\\Downloads\\win10_pic\\1920x1080"

# # Call the function to convert the video to images
# convert_video_to_images(video_path, output_folder)