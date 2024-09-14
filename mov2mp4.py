import os
import json
from moviepy.editor import VideoFileClip


def convert_mov_to_mp4(pathVideos):

    # List all files in the input folder
    for filename in os.listdir(pathVideos):
        if filename.lower().endswith('.mov'):
            # Define full path for the input and output files
            input_path = os.path.join(pathVideos, filename)
            output_filename = os.path.splitext(filename)[0] + '.mp4'
            output_path = os.path.join(pathVideos, output_filename)

            print(f'Converting {input_path} to {output_path}')

            # Load the .mov file and write it to .mp4 format
            with VideoFileClip(input_path) as video:
                video.write_videofile(output_path, codec='libx264', audio_codec='aac')


def main():
    # import json
    with open("config.json") as file:
        configData = json.load(file)

    # select project
    projectName = configData["project"]["projectName"]
    run = "run_" + str(configData["project"]["run"])

    ### define paths
    pathDatasets = configData["paths"]["datasets"]
    pathProject = os.path.join(pathDatasets, projectName)
    pathRun = os.path.join(pathProject, run)
    pathVideos = os.path.join(pathRun, 'videos')

    # convert
    convert_mov_to_mp4(pathVideos)


if __name__ == "__main__":
    main()