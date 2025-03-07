import torch 
import torchvision.transforms as transforms


RESIZE_SIZE = (64, 64)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # Device 
NB_EPOCHS = 30 # Number of epochs for training 
BATCH_SIZE = 15  # Size of the training batch
TRAINING_IMAGE_FILE_PATH = "./data/train/images/"
TRAINING_LABEL_FILE_PATH = "./data/train/labels/"
VAL_IMAGE_FILE_PATH = "./data/val/images/"
VAL_LABEL_FILE_PATH = "./data/val/labels/"

TRANFORMATIONS = transforms.Compose([transforms.Resize((64,64)),
                                     transforms.ToTensor(),
                                     transforms.Normalize(mean=[0.4914, 0.4822, 0.4465],
                                                          std=[0.2023, 0.1994, 0.2010])
                                     ])