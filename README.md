# YOLO Half-Automatic Labelling Pipeline

This repository contains a Python pipeline for automating the labelling process of object detection models, particularly for YOLO (You Only Look Once). The pipeline iterates over a video dataset, extracts frames, labels them manually using **labelImg**, and then uses the output of a YOLOv8 model to assist in labelling the next dataset. With each iteration, the model's predictions improve, speeding up the labelling process.

## Workflow Overview

The labelling process is iterative, starting with a recorded video. A small dataset of frames is extracted, labelled manually, and split into training, validation, and test sets. The YOLOv8 model is trained with the labelled data, and the detection output is used to label the next dataset.

The goal is to improve the accuracy and speed of labelling through each iteration, gradually reducing the amount of manual work required.

### Desired Output Format

1. **Label File (YOLO Format)**: 
   
   The labels are stored in the YOLO format as two `.txt` files for each image. The filenames follow the format: `videoNr_imageNr.txt` (e.g., `05_0609.txt`). 
   Example of the label file contents:

      ```txt
      0 0.510648 0.373958 0.013889 0.007292
      1 0.588426 0.372656 0.010185 0.004687
      2 0.812037 0.473698 0.016667 0.008854
      3 0.819907 0.516667 0.015741 0.008333
      ```
   
2. **Classes File:** A classes.txt file that defines the object classes. Each line corresponds to a different class ID:
   ```
   0
   1
   2
   3
   4
   5
   6
   7
   0
   ```
These label and class files need to be manually adjusted during labelling, and the output improves with each iteration of the pipeline.
   


## Pipeline Scripts

The following scripts are used to perform the labelling process:
- `requirements.txt`: Contains the list of Python dependencies required to run the scripts.
- `config.json`: Configuration file containing the necessary settings for the pipeline.
- `recordVideo.py`: Script to record video for the dataset.
- `mov2mp4.py`: Script to convert recorded video files into `.mp4` format.
- `extractFrames.py`: Script to extract frames from recorded videos.
- `createDatasetYolo.py`: Script to create a YOLO-compatible dataset from video frames.
- `labelFramesYolo.py`: Script to manually label frames using **labelImg**.
- `mergeLabels.py`: Script to merge the labelled dataset for each class after manual labelling.
- `train.py`: Script to train the YOLOv8 model on the labelled dataset.
- `export2openvino.py`: Script to convert the YOLOv8 model to OpenVINO format for optimized inference.
- `detect.py`: Script to run the YOLO model and perform detection on frames to generate initial labels.

## Process Explanation

1. **Record Video**: Use `recordVideo.py` to record a video, which will be used as the dataset.
2. **Extract Frames**: Use `extractFrames.py` to extract a specific number of frames from the video.
3. **Manual Labelling**: Label the extracted frames using **labelImg**. During labelling, the same class should be labelled sequentially for faster processing.
4. **Split Dataset**: Split the labelled dataset into training, validation, and test sets, using a 70-15-15% split ratio.
5. **Model Training**: Train the YOLOv8 model using `train.py` on the labelled data.
6. **Label Next Dataset**: Use the model's predictions to assist in labelling the next dataset.
7. **Merge Labels**: After labelling, run `mergeLabels.py` to combine all the labelled data together into a unified format.

## Benefits

The iterative nature of this process allows the model's predictions to improve with each cycle, reducing the amount of manual labelling required. The key advantage of this approach is the significant speedup in labelling through the use of semi-automatic predictions from the model, allowing you to focus on adjusting the labels rather than creating them from scratch.

By labelling the same class sequentially across images, the process is further accelerated. The `mergeLabels.py` script consolidates all labelled data from different classes into a single dataset, ready for use in further iterations.

## Installation

To get started with this pipeline, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/JBrakel/createDatasets.git
cd createDatasets
pip install -r requirements.txt
```

## Requirements

The project requires the following Python libraries, which can be installed from `requirements.txt`:

- `numpy`
- `opencv-python`
- `labelImg`
- `ultralytics` (for YOLOv8)
- `openvino` (for model export)
- Other dependencies listed in `requirements.txt`

## Conclusion

This pipeline helps streamline the labelling process for YOLO model training by combining manual labelling and model predictions. With each iteration, the model's performance improves, making the labelling process faster and more efficient.

For any issues or contributions, feel free to open an issue or submit a pull request!
