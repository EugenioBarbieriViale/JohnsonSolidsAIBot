from os import path, mkdir
import pandas as pd
from random import randint

import webscrape
import neural_network

dirname = "../data/"

f1 = dirname + "names.csv"
f2 = dirname + "image_urls.csv"
imgs_dir = dirname + "images/" # remember to put / at the end

# root = "linear_1000"
# root = "conv_500"
root = "linear_2500"

model_file = f"../models/{root}.pth"
graph_name = f"../graphs/{root}.png"


w = webscrape.Webscrape()

if not path.isfile(f1):
    names = w.get_names()
    w.save(f1, names)
    print("Names saved to file", f1)

if not path.isfile(f2):
    urls = w.get_image_urls()
    w.save(f2, urls)
    print("URLs saved to file", f2)

if not path.isdir(imgs_dir):
    mkdir(imgs_dir)
    w.download_images(imgs_dir)
    print("Images downloaded to directory:", imgs_dir)
    
names = pd.read_csv(f1).values.flatten()
index = randint(0, 91)

nn = neural_network.JS_Classifier()

nn.learn(epochs=2500, filename=model_file, imgname=graph_name, save=True)
nn.load(filename=model_file)

nn.test()
nn.predict(index, names)
