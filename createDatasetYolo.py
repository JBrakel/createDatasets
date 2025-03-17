import os
import shutil
from sklearn.model_selection import train_test_split
from ultralytics import YOLO
import cv2
import math
import cvzone
import json

def createDatasetYolo(path_run, class_names, split_ratios=[0.7, 0.15, 0.15]):
    path_images = os.path.join(path_run, 'images')
    path_labels = os.path.join(path_run, 'labels')
    path_yolo = os.path.join(path_run, 'yolov8')

    if not os.path.exists(path_yolo):
        os.makedirs(path_yolo)

    splits = ['train', 'test', 'valid']
    sub_folders = ['images', 'labels']

    data_splitted = split_dataset(path_images, path_labels, split_ratios)

    for split in splits:
        path_split = os.path.join(path_yolo, split)
        if not os.path.exists(path_split):
            os.makedirs(path_split)

        for sub in sub_folders:
            path_run_sub = os.path.join(path_run, sub)
            path_yolo_split_sub = os.path.join(path_split, sub)

            if not os.path.exists(path_yolo_split_sub):
                os.makedirs(path_yolo_split_sub)

            for file in data_splitted[f"{split}"][f"{sub}"]:
                src = os.path.join(path_run_sub, file)
                dst = os.path.join(path_yolo_split_sub, file)
                shutil.copy(src, dst)

    create_yaml_file(path_run, class_names)

def split_dataset(path_all_images, path_all_labels,split_ratios):

    list_all_images = sorted([f for f in os.listdir(path_all_images) if f.endswith('.jpg')])
    list_all_labels = sorted([f for f in os.listdir(path_all_labels) if f.endswith('.txt') and f != 'classes.txt'])

    train_ratio = split_ratios[0]
    test_ratio = split_ratios[1]
    valid_ratio = split_ratios[2]


    train_images, test_images, train_labels, test_labels = train_test_split(list_all_images, list_all_labels,
                                                                            test_size=test_ratio + valid_ratio)

    valid_images, test_images, valid_labels, test_labels = train_test_split(test_images, test_labels,
                                                                            test_size=valid_ratio / (
                                                                                        test_ratio + valid_ratio))

    data_splitted = {
        'train': {
            'images': train_images,
            'labels': train_labels
        },
        'test': {
            'images': test_images,
            'labels': test_labels
        },
        'valid': {
            'images': valid_images,
            'labels': valid_labels
        }
    }

    return data_splitted

def create_yaml_file(path_run, cls):
    path_yolo = os.path.join(path_run, 'yolov8')
    # temp_path = "/Users/jannisbrakel"
    # path = '../drive/MyDrive' + path_yolo[len(temp_path):]
    temp_path = "/home/jannis"
    path = ".." + path_yolo[len(temp_path):]
    path_text_file = os.path.join(path_yolo, "data.txt")
    path_yaml_file = os.path.join(path_yolo, "data.yaml")

    nc = len(cls)
    data = {
        'path': path,
        'train': '../train/images',
        'val': '../valid/images',
        'test': '../test/images',
        'nc': nc,
        'names': cls
    }

    text_data = f"path: {data['path']}\n"
    text_data += f"train: {data['train']}\n"
    text_data += f"val: {data['val']}\n"
    text_data += f"test: {data['test']}\n"
    text_data += f"\nnc: {data['nc']}\n"
    text_data += f"names: {data['names']}\n"

    with open(path_text_file, 'w') as text_file:
        text_file.write(text_data)

    os.rename(path_text_file, path_yaml_file)


def change_first_number_to_zero(folder_path):
    for filename in sorted(os.listdir(folder_path)):
        print(filename)
        if filename.endswith('.txt') and filename != "classes.txt":
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r') as file:
                lines = file.readlines()

            modified_lines = []
            for line in lines:
                parts = line.split()
                print(line, parts)
                if len(parts) > 0 and parts[0] in ['0', '1']:  # Added check to ensure parts is not empty
                    parts[0] = '0'
                modified_line = ' '.join(parts)
                modified_lines.append(modified_line)

            with open(file_path, 'w') as file:
                file.write('\n'.join(modified_lines) + '\n')
        print('---')


def main():
    # import json
    with open("config.json") as file:
        configData = json.load(file)

    # select project
    projectName = configData["project"]["projectName"]
    run = "run_" + str(configData["project"]["run"])

    # define dataset
    classNames = configData["yolo"]["classNames"]
    splitRatio = configData["dataset"]["splitRatio"]

    ### define paths
    pathDatasets = configData["paths"]["datasets"]
    pathProject = os.path.join(pathDatasets, projectName)
    pathRun = os.path.join(pathProject, run)

    createDatasetYolo(pathRun, classNames, splitRatio)

if __name__ == "__main__":
    main()