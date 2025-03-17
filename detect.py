from ultralytics import YOLO
import cv2
import math
import cvzone
import json
import os

def start_frame(video_path, start_frame):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    return cap

def display_frame_number(img, frame_number):
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottom_left_corner = (10, img.shape[0] - 10)
    font_scale = 1
    font_color = (255, 255, 255)
    line_type = 2

    cv2.putText(img, f'Frame: {frame_number}',
                bottom_left_corner,
                font,
                font_scale,
                font_color,
                line_type)
    return img

if __name__ == "__main__":

    ################################################################################################

    # video
    pathVideo = ...

    ################################################################################################


    # import json
    with open("config.json") as file:
        configData = json.load(file)

    # select project
    projectName = configData["project"]["projectName"]
    run = "run_" + str(configData["project"]["run"])

    # define dataset
    classNames = configData["yolo"]["classNames"]
    model = configData["yolo"]["model"][0]

    # define paths
    pathDatasets = configData["paths"]["datasets"]
    pathProject = os.path.join(pathDatasets, projectName)
    pathRun = os.path.join(pathProject, run)
    pathImages = os.path.join(pathRun, 'images')
    pathWeights = os.path.join(pathRun,f"yolov8/{run}{model}.pt")

    cap = start_frame(pathVideo, 0)
    model = YOLO(pathWeights)

    if cap.isOpened():

        while True:
            ret, img = cap.read()

            if not ret:
                break

            result = model(img, stream=True)

            for r in result:
                boxes = r.boxes
                for box in boxes:

                    # bb
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # confidence
                    conf = math.ceil((box.conf[0] * 100)) / 100

                    # class name
                    cls = box.cls[0]
                    # current_class = classNames[int(cls)]

                    # if current_class == 'db':
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    # cvzone.putTextRect(img, f"{current_class} {conf}", (max(0, x1), max (35,y1)), scale=3, thickness=3)


            scale = 0.5
            img = display_frame_number(img, int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
            cv2.namedWindow("output", cv2.WINDOW_NORMAL)
            cv2.imshow("output", img)
            cv2.resizeWindow("output", int(img.shape[1] * scale), int(img.shape[0] * scale))
            cv2.moveWindow("output", 0, 0)

            # quit video
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break