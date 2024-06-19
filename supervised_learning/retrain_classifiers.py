from utils.utils import *
from supervised_learning.utils import *
from supervised_learning.config import *
from joblib import load
import argparse 

# ------------- IMPORT PARSER & ARGS ---------------

parser = argparse.ArgumentParser()
parser.add_argument('predicted_label_folder', metavar='DIR', help='Folder of input images to analyse')

# Analyser les arguments de la ligne de commande
args = parser.parse_args()

# Load predicted label folder folder
predicted_label_folder = args.predicted_label_folder
# Check if input folder exists
if not os.path.exists(predicted_label_folder):
    raise FileNotFoundError(f"[Error] Folder '{predicted_label_folder}' does not exist.")


print(f"[TRAIN FP] Start re-training on false positives with {predicted_label_folder} folder")

# ------------- LOAD CLASSIFIERS -----------------
# Dict format to store all classifiers
classifiers = {
    "danger" : None, 
    "interdiction": None,
    "obligation": None, 
    "stop": None,
    "ceder": None, 
    "frouge": None, 
    "forange": None, 
    "fvert": None
}

# Parse dict and load all classifiers
print("[TRAIN FP] Loading classifiers...")
for classe in classifiers.keys():
    if classe not in ['ff', 'empty']:
        classifiers[classe] = load(f"{CLASSIFIERS_FOLDER_PATH}/SVM_{classe}.joblib")

# ------------- LOAD DATAS -----------------
print("[TRAIN FP] Loading input datas...")

# 1. Load real labels
real_labels = {}   # Dict with all the real label linked with the image name
# Load real labels
for filename in os.listdir(TRAINING_LABEL_FOLDER_PATH):
    name = filename.split(".")[0]
    filepath = os.path.join(TRAINING_LABEL_FOLDER_PATH, filename)

    real_labels[name] = []
    with open(filepath, "r") as label_file:
        rows = label_file.readlines()
        if rows != ['\n']:
            for row in rows:
                row = row.strip().split(",")
                xmin, ymin, xmax, ymax = map(int, row[0:4])
                class_name = row[4]
                real_labels[name].append([xmin, ymin, xmax, ymax, class_name])
                    
# 2. Load images
images = {}
for filename in os.listdir(TRAINING_IMAGE_FOLDER_PATH):
    name = filename.split(".")[0]
    filepath = os.path.join(TRAINING_IMAGE_FOLDER_PATH, filename)
    image = Image.open(filepath)
    images[name] = image


# 3. Load predicted labels
predicted_labels = {} # Dict with all the label predicted linked with the image name
# Load predicted datas
for filename in os.listdir(predicted_label_folder):
    name = filename.split(".")[0]
    filepath = os.path.join(predicted_label_folder, filename)

    predicted_labels[name] = []
    with open(filepath, "r") as label_file:
        for row in label_file.readlines():
            row = row.split(",")
            predicted_labels[name].append([int(row[0]), int(row[1]), int(row[2]), int(row[3]), row[4]])


# ------------- ANALYSIS OF THE PREDICTIONS & CREATION OF NEW DATASETS -----------------
datasets = {
    "danger" : {
        "X" : [],
        "Y" : []
    }, 
    "interdiction": {
        "X" : [],
        "Y" : []
    },
    "obligation": {
        "X" : [],
        "Y" : []
    }, 
    "stop": {
        "X" : [],
        "Y" : []
    },
    "ceder": {
        "X" : [],
        "Y" : []
    }, 
    "frouge": {
        "X" : [],
        "Y" : []
    }, 
    "forange": {
        "X" : [],
        "Y" : []
    }, 
    "fvert":{
        "X" : [],
        "Y" : []
    }
}

for key in real_labels.keys():
    reality = real_labels[key]
    prediction = predicted_labels[key]

    print("Img processed : ", images[name], "Real labels are : ", reality, " || Predicted labels are : ", prediction)