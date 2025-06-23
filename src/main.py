from os import path, mkdir
import pandas as pd
from random import randint

import telebot
from telebot import types

import webscrape
import neural_network
import levels_bot


dirname = "../data/"

f1 = dirname + "names.csv"
f2 = dirname + "image_urls.csv"
imgs_dir = dirname + "images/" # remember to put / at the end

epochs = 2500
# epochs = 1000
# epochs = 500
# epochs = 250
# epochs = 100

root = f"linear_{epochs}"

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

def run(names):
    index = randint(0, 91)

    nn.learn(epochs=epochs, filename=model_file, imgname=graph_name, save=True)
    nn.load(filename=model_file)

    nn.test()
    nn.predict(index, names)

nn = neural_network.JS_Classifier()

with open("../token_file.txt", "r") as f:
    token = f.read()

token = token.replace("\n", "")
bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=["start"])
def send_welcome(message):
	bot.send_message(message.chat.id, "Welcome! Are you ready to challenge AI in recognising Johnson solids?", parse_mode="Markdown")

@bot.message_handler(commands=["levels"])
def show_levels(message):
    msg = []
    for i in range(0, 5):
        msg.append(levels_bot.show_bot_level(i+1))
        msg.append("\n")
    bot.reply_to(message, "".join(msg))

@bot.message_handler(commands=["choose"])
def choose_level(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)

    l1 = types.KeyboardButton("/very_easy")
    l2 = types.KeyboardButton("/easy")
    l3 = types.KeyboardButton("/medium")
    l4 = types.KeyboardButton("/difficult")
    l5 = types.KeyboardButton("/impossible")

    markup.add(l1, l2, l3, l4, l5)
    bot.reply_to(message, "Choose a level:", reply_markup=markup)

    markup = types.ReplyKeyboardRemove(selective=False)

levels = ["very_easy", "easy", "medium", "difficult", "impossible"]

@bot.message_handler(commands=[f"{levels[0]}"])
def load_l1(message):
    bot.reply_to(message, f"Loading {levels[0]} version")

@bot.message_handler(commands=[f"{levels[1]}"])
def load_l2(message):
    bot.reply_to(message, f"Loading {levels[1]} version")

@bot.message_handler(commands=[f"{levels[2]}"])
def load_l3(message):
    bot.reply_to(message, f"Loading {levels[2]} version")

@bot.message_handler(commands=[f"{levels[3]}"])
def load_l4(message):
    bot.reply_to(message, f"Loading {levels[3]} version")

@bot.message_handler(commands=[f"{levels[4]}"])
def load_l5(message):
    bot.reply_to(message, f"Loading {levels[4]} version")

@bot.message_handler(commands=["model"])
def show_model(message):
    bot.reply_to(message, str(nn.show_model()))

bot.infinity_polling()
