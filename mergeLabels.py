import os
import json

def mergeLabels(path_run, pathLabels):

    if not os.path.exists(pathLabels):
        os.makedirs(pathLabels)

    folders_labels = sorted(os.listdir(path_run))
    folders_labels = [f for f in folders_labels if f.startswith('labels_')]

    merged_files = {}
    all_cls = []

    # loop through each folder with labels of single class -> "labels_cups"
    for i, file_name in enumerate(folders_labels):
        path_labels_single_class = os.path.join(path_run, f'{file_name}')
        files_txt = sorted(os.listdir(path_labels_single_class))
        files_txt = [f for f in files_txt if f.endswith('.txt')]

        # find classes.txt file to extract class number -> cls
        all_cls = extract_class_nr(path_labels_single_class, files_txt, all_cls)

        # save this in merged_files/modified lines
        cls = all_cls[i]
        save_merged_files(path_labels_single_class, files_txt, cls, merged_files)

    # create single "classes.txt" file for every class -> saved in "labels"
    path_new_classes_file = os.path.join(pathLabels, 'classes.txt')
    with open(path_new_classes_file, 'w') as text_file:
        text_file.write('\n'.join(all_cls) + '\n')

    # create single .txt file with every class and bb infos for every image -> saved in "labels"
    for f_txt, lines in merged_files.items():
        path_new_test_file = os.path.join(pathLabels, f_txt)
        with open(path_new_test_file, 'w') as text_file:
            text_file.write('\n'.join(lines) + '\n')

def extract_class_nr(path_labels_single_class, files_txt, all_cls):
    for f_txt in files_txt:
        if f_txt == ('classes.txt'):
            path_text_file = os.path.join(path_labels_single_class, f_txt)
            with open(path_text_file, 'r') as text_file:
                cls = text_file.read().strip()
                all_cls.append(cls)
    return all_cls

def save_merged_files(path_labels_single_class, files_txt, cls, merged_files):
    for f_txt in files_txt:
        if f_txt != ('classes.txt'):
            path_text_file = os.path.join(path_labels_single_class, f_txt)

            with open(path_text_file, 'r') as text_file:
                lines = text_file.readlines()

            modified_lines = replace_cls(lines, cls)

            if f_txt not in merged_files:
                merged_files[f_txt] = []

            merged_files[f_txt].extend(modified_lines)

def replace_cls(lines, cls):
    modified_lines = []
    for line in lines:
        chars = line.split()
        if chars:
            chars[0] = cls
            modified_line = ' '.join(chars)
            modified_lines.append(modified_line)
    return modified_lines


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
    pathLabels = os.path.join(pathRun, 'labels')

    # merge all labels into single folder
    mergeLabels(pathRun, pathLabels)



if __name__ == "__main__":
    main()