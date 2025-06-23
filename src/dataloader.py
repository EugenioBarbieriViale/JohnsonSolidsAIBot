from os import walk, path 
from numpy import array
from cv2 import imread, resize, INTER_AREA

import torch
from torchvision.transforms import Compose, ToTensor, Normalize


class JS_Dataset():
    def __init__(self, data_path="../data/images", labels_path="../data/names.csv"):
        super().__init__()

        resize_img = 64

        imgs = []
        for root, sub, file in walk(data_path):
            for f in file:
                filepath = path.join(root, f)
                img = imread(filepath, 0) # 0 is grayscale
                img = imread(filepath)

                img = resize(img, (resize_img, resize_img), interpolation=INTER_AREA)
                imgs.append(img[:,:,0])

        labels_onehot = torch.zeros(size=(92, 92))
        for idx, label in enumerate(labels_onehot):
            labels_onehot[idx][idx] = 1

        self._dataset = array(imgs)
        self.labels = labels_onehot

    def __getitem__(self, index):
        transform = Compose([
            ToTensor(),
            Normalize([0.485], [0.229])
        ])

        x = self._dataset[index]
        y = self.labels[index]

        return transform(x), y

    def __len__(self):
        return len(self._dataset)
