import os
from ultralytics import YOLO
import cv2
import json

def labelFramesYolo(path_run, path_images, path_weights, class_names):
    model = YOLO(path_weights)
    images = sorted([f for f in os.listdir(path_images) if f.endswith(".jpg")])
    class_names_without_spaces = [c.replace(' ', '_') for c in class_names]
    for i, name in enumerate(class_names_without_spaces):
        path_label_class = os.path.join(path_run, f"labels_{name}")

        if not os.path.exists(path_label_class):
            os.makedirs(path_label_class)

        path_file_classes_txt = os.path.join(path_label_class, 'classes.txt')
        cls_id = i
        with open(path_file_classes_txt, 'w') as text_file:
            text_file.write(f"{cls_id}")

        for image in images:
            image_name = image.split('.')[0]
            path_img = os.path.join(path_images, image)
            path_file_video_txt = os.path.join(path_label_class, f'{image_name}.txt')

            result = model(path_img, stream=True)
            img = cv2.imread(path_img)
            bb_string_list = save_bb_cxcywh(result, cls_id, img, class_names)

            with open(path_file_video_txt, 'w') as text_file:
                text_file.write('\n'.join(bb_string_list))

            print(f"class: {i+1}/{len(class_names_without_spaces)}, {image} finished")

def save_bb_cxcywh(result, cls_id, img, class_names):
    img_height, img_width, _ = img.shape
    bb_string_list = []
    for r in result:
        boxes = r.boxes
        for box in boxes:
            cls = box.cls[0]
            current_class = class_names[int(cls)]

            if current_class != class_names[cls_id]:
                continue

            cx, cy, w, h = box.xywh[0]

            cx_norm = cx / img_width
            cy_norm = cy / img_height
            w_norm = w / img_width
            h_norm = h / img_height

            bb_string = f"0 {cx_norm} {cy_norm} {w_norm} {h_norm}"
            bb_string_list.append(bb_string)
    return bb_string_list

def main():

    # import json
    with open("config.json") as file:
        configData = json.load(file)

    # select project
    projectName = configData["project"]["projectName"]
    run = "run_" + str(configData["project"]["run"])

    # define dataset
    classNames = configData["yolo"]["classNames"]

    # define paths
    pathDatasets = configData["paths"]["datasets"]
    pathProject = os.path.join(pathDatasets, projectName)
    pathRun = os.path.join(pathProject, run)
    pathImages = os.path.join(pathRun, 'images')
    model = configData["yolo"]["model"][0]

    # path to weights from previous run -> "best available weights"
    NrPreviousRun = int(run.split('_')[1]) - 1

    if NrPreviousRun < 0:
        NrPreviousRun = 0

    previousRun = f"run_{NrPreviousRun}/yolov8/run_{NrPreviousRun}{model}.pt"
    pathWeights = os.path.join(pathProject, previousRun)

    labelFramesYolo(pathRun, pathImages, pathWeights, classNames)
    print(f"\nlabels created with run_{NrPreviousRun}{model}.pt")

if __name__ == "__main__":
    main()
