import os
import cv2
import json


def extractFrames(path_videos, path_images, start_seconds, stop_seconds, total_frames):
    if not os.path.exists(path_images):
        os.makedirs(path_images)

    video_files = [f for f in os.listdir(path_videos) if f.startswith('video_')]
    video_files.sort()

    for video in video_files:
        path_video = os.path.join(path_videos, video)
        video_name, _ = os.path.splitext(video)
        video_number = video_name.split('_')[1]

        cap = cv2.VideoCapture(path_video)
        if not cap.isOpened():
            print(f"Failed to open {video}")
            continue

        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if start_seconds is None:
            start_seconds = 0
        if stop_seconds is None:
            stop_seconds = frame_count / frame_rate

        start_frame = int(start_seconds * frame_rate)
        stop_frame = int(stop_seconds * frame_rate)

        if start_frame >= frame_count:
            print(f"Start frame {start_frame} is beyond the total frames in {video}")
            cap.release()
            continue

        if stop_frame >= frame_count:
            stop_frame = frame_count - 1

        if total_frames > 1:
            frame_interval = (stop_frame - start_frame) / (total_frames - 1)
        else:
            frame_interval = stop_frame - start_frame

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        frames_extracted = 0

        while True:
            frame_pos = int(start_frame + frame_interval * frames_extracted)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            ret, frame = cap.read()

            if not ret or frame_pos > stop_frame:
                break
            frame_filename = os.path.join(path_images, f"{video_number}_{frame_pos:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            frames_extracted += 1

        print(f"{video} finished")
        cap.release()


def main():
    # Load configuration
    with open("config.json") as file:
        configData = json.load(file)

    # Select project
    projectName = configData["project"]["projectName"]
    run = "run_" + str(configData["project"]["run"])

    # Define dataset
    startSecond = configData["dataset"]["startSecond"]
    stopSecond = configData["dataset"]["stopSecond"]
    totalFrames = configData["dataset"]["totalFrames"]

    ### Define paths
    pathDatasets = configData["paths"]["datasets"]
    pathProject = os.path.join(pathDatasets, projectName)
    pathRun = os.path.join(pathProject, run)
    pathImages = os.path.join(pathRun, 'images')
    pathVideos = os.path.join(pathRun, 'videos')

    # Extract frames from all videos
    extractFrames(pathVideos, pathImages,
                  start_seconds=startSecond,
                  stop_seconds=stopSecond,
                  total_frames=totalFrames)


if __name__ == "__main__":
    main()