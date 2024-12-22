from ultralytics import YOLO
import os
import json

def main():

    # import json
    with open("config.json") as file:
        configData = json.load(file)

    # select project
    projectName = configData["project"]["projectName"]
    run = "run_" + str(configData["project"]["run"])

    # define paths
    pathDatasets = configData["paths"]["datasets"]
    pathProject = os.path.join(pathDatasets, projectName)
    pathRun = os.path.join(pathProject, run)
    # pathWeights = configData["paths"]["weights"]
    pathYamlFile = os.path.join(pathRun, "yolov8/data.yaml")
    # print(pathWeights)
    # path to weights from previous run -> "best available weights"
    NrPreviousRun = int(run.split('_')[1]) - 1

    if NrPreviousRun < 0:
        NrPreviousRun = 0

    model = configData["yolo"]["model"][0]
    previousRun = f"run_{NrPreviousRun}/yolov8/run_{NrPreviousRun}{model}.pt"
    pathPreviousWeights = os.path.join(pathProject, previousRun)

    # if not pathWeights:
    pathWeights = pathPreviousWeights

    model = YOLO(pathWeights)
    model.train(data=pathYamlFile, epochs=50, imgsz=640)


if __name__ == "__main__":
    main()

