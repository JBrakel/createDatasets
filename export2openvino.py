import json
import os
from ultralytics import YOLO

def main():
    # import json
    with open("config.json") as file:
        configData = json.load(file)

    # select project
    projectName = configData["project"]["projectName"]
    run = "run_" + str(configData["project"]["run"])
    model = configData["yolo"]["model"][0]

    # define paths
    pathDatasets = configData["paths"]["datasets"]
    pathProject = os.path.join(pathDatasets, projectName)
    pathRun = os.path.join(pathProject, run)
    pathWeights = os.path.join(pathRun,f"yolov8/{run}{model}.pt")

    model = YOLO(pathWeights)
    model.export(format="openvino")

if __name__ == "__main__":
    main()