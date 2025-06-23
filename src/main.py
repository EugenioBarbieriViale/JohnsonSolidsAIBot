from os import path, mkdir
import pandas as pd
from random import randint, shuffle

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
    bot.send_message(message.chat.id, "Type /help to list possible commands", parse_mode="Markdown")

@bot.message_handler(commands=["help", "h"])
def help(message):
    l1 = "Commands:\n"
    l2 = "/model - show the neural network's architecture\n"
    l3 = "/levels - show different difficulties of the neural network\n"
    l4 = "/choose - choose difficulties\n"
    l5 = "/play or /p - play\n"
    l6 = "/reset - reset both scores\n"
    lf = "\nRemember to choose a level (/choose), otherwise no model will be loaded\n"
    msg = l1 + l2 + l3 + l4 + l5 + l6 + lf
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=["model"])
def show_model(message):
    bot.reply_to(message, str(nn.show_model()))

@bot.message_handler(commands=["levels"])
def show_levels(message):
    msg = []
    for i in range(0, 5):
        msg.append(levels_bot.show_bot_level(i+1))
        msg.append("\n")
    bot.reply_to(message, "".join(msg))

levels = ["very_easy", "easy", "medium", "difficult", "impossible"]

@bot.message_handler(commands=["choose"])
def choose_level(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)

    l1 = types.KeyboardButton("/" + levels[0])
    l2 = types.KeyboardButton("/" + levels[1])
    l3 = types.KeyboardButton("/" + levels[2])
    l4 = types.KeyboardButton("/" + levels[3])
    l5 = types.KeyboardButton("/" + levels[4])

    markup.add(l1, l2, l3, l4, l5)
    bot.reply_to(message, "Choose a level:", reply_markup=markup)

    markup = types.ReplyKeyboardRemove(selective=False)

@bot.message_handler(commands=[levels[0]])
def load_l1(message):
    nn.load(filename="../models/linear_100.pth")
    bot.reply_to(message, f"Loaded {levels[0]} version")

@bot.message_handler(commands=[levels[1]])
def load_l2(message):
    nn.load(filename="../models/linear_250.pth")
    bot.reply_to(message, f"Loaded {levels[1]} version")

@bot.message_handler(commands=[levels[2]])
def load_l3(message):
    nn.load(filename="../models/linear_500.pth")
    bot.reply_to(message, f"Loaded {levels[2]} version")

@bot.message_handler(commands=[levels[3]])
def load_l4(message):
    nn.load(filename="../models/linear_1000.pth")
    bot.reply_to(message, f"Loaded {levels[3]} version")

@bot.message_handler(commands=[levels[4]])
def load_l5(message):
    nn.load(filename="../models/linear_2500.pth")
    bot.reply_to(message, f"Loaded {levels[4]} version")

score = 0
ai_score = 0

@bot.message_handler(commands=["reset"])
def reset(message):
    global score, ai_score
    score = 0
    ai_score = 0
    bot.reply_to(message, f"Your score is: {score} \n AI's score is: {ai_score}")

@bot.message_handler(commands=["play", "p"])
def play(message):
    idx = randint(1, 89)

    correct = str(names[idx]).replace(" ", "_")
    options = [str(names[idx-1]).replace(" ", "_"), correct, str(names[idx+1]).replace(" ", "_")]

    name = str(names[idx]).replace(" ", "_")
    if "bipyramid" in name:
        name = name.replace("bipyramid", "dipyramid")

    img = open("../data/images/" + name + ".png", "rb")
    bot.send_photo(message.chat.id, img)

    shuffle(options)

    markup = types.ReplyKeyboardMarkup(row_width=1)

    o1 = types.KeyboardButton("/" + options[0])
    o2 = types.KeyboardButton("/" + options[1])
    o3 = types.KeyboardButton("/" + options[2])
    markup.add(o1, o2, o3)

    bot.reply_to(message, "Choose an option:", reply_markup=markup)

    @bot.message_handler(commands=options)
    def verify(message):
        global score, ai_score
        nonlocal idx

        if message.text[1:] == correct:
            bot.reply_to(message, "Correct!")
            score += 1
        else:
            bot.reply_to(message, "Incorrect!")
            if score != 0:
                score -= 1

        predicted = nn.predict(idx, names, plot=False).replace(" ", "_")
        if predicted == correct:
            ai_score += 1
        else:
            if ai_score != 0:
                ai_score -= 1

        bot.send_message(message.chat.id, f"AI answered: {predicted}")
        bot.send_message(message.chat.id, f"The right answer is: {correct}")

        bot.send_message(message.chat.id, f"Your score is: {score} \n AI's score is: {ai_score}")


print("Bot is up!")
bot.infinity_polling()
