from os import path, mkdir, execv
import sys
from requests.exceptions import ConnectionError, ReadTimeout

from datetime import datetime
import pandas as pd
from random import randint, shuffle

import telebot
from telebot import types

import webscrape
import neural_network
import levels_bot


dirname = "../data/"

names_file = dirname + "names.csv"
imgs_dir = dirname + "images/" # remember to put / at the end

w = webscrape.Webscrape()

if not path.isfile(names_file):
    names = w.get_names()
    w.save(name_files, names)
    print("Names saved to file", names_file)

if not path.isdir(imgs_dir):
    mkdir(imgs_dir)
    w.download_images(imgs_dir)
    print("Images downloaded to directory:", imgs_dir)

names = pd.read_csv(names_file).values.flatten()

nn = neural_network.JS_Classifier()

with open("../token_file.txt", "r") as f:
    token = f.read()

token = token.replace("\n", "")
bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    username = str(message.from_user.username)

    bot.send_message(message.chat.id, f"Welcome @{username}! Are you ready to challenge AI in recognising Johnson solids?", parse_mode="Markdown")
    bot.send_message(message.chat.id, "Type /help to list possible commands", parse_mode="Markdown")

    d = str(datetime.now())
    with open("../users.txt", "a") as f:
        print(f"{username} has connected - {d}")
        f.write(username + ": " + d + "\n")

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


@bot.message_handler(commands=[levels[0]])
def load_l1(message):
    username = str(message.from_user.username)
    nn.load(filename="../models/linear_100.pth")
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, f"Loaded {levels[0].replace('_', ' ')} version", reply_markup=markup)
    print(f"{username} has loaded very easy model")

@bot.message_handler(commands=[levels[1]])
def load_l2(message):
    username = str(message.from_user.username)
    nn.load(filename="../models/linear_250.pth")
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, f"Loaded {levels[1].replace('_', ' ')} version", reply_markup=markup)
    print(f"{username} has loaded easy model")

@bot.message_handler(commands=[levels[2]])
def load_l3(message):
    username = str(message.from_user.username)
    nn.load(filename="../models/linear_500.pth")
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, f"Loaded {levels[2].replace('_', ' ')} version", reply_markup=markup)
    print(f"{username} has loaded medium model")

@bot.message_handler(commands=[levels[3]])
def load_l4(message):
    username = str(message.from_user.username)
    nn.load(filename="../models/linear_1000.pth")
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, f"Loaded {levels[3].replace('_', ' ')} version", reply_markup=markup)
    print(f"{username} has loaded difficult model")

@bot.message_handler(commands=[levels[4]])
def load_l5(message):
    username = str(message.from_user.username)
    nn.load(filename="../models/linear_2500.pth")
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, f"Loaded {levels[4].replace('_', ' ')} version", reply_markup=markup)
    print(f"{username} has loaded impossible model")

score = 0
ai_score = 0

@bot.message_handler(commands=["reset"])
def reset(message):
    global score, ai_score
    score = 0
    ai_score = 0
    bot.reply_to(message, f"Your score is: {score}\nAI's score is: {ai_score}")

idxs = []

@bot.message_handler(commands=["play", "p"])
def play(message):
    username = str(message.from_user.username)
    idx = randint(1, 89)
    idxs.append(idx)

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
    print(f"{username} is playing: score: {score}, ai_score: {ai_score}")

    @bot.message_handler(func=lambda message: True)
    def verify(message):
        global score, ai_score

        idx = idxs[-1]

        markup = types.ReplyKeyboardRemove(selective=False)
        if message.text[1:] == correct:
            bot.reply_to(message, "Correct!", reply_markup=markup)
            score += 1
        else:
            bot.reply_to(message, "Incorrect!", reply_markup=markup)
            if score != 0:
                score -= 1

        predicted = nn.predict(idx, names, plot=False).replace(" ", "_")
        if predicted == correct:
            ai_score += 1
        else:
            if ai_score != 0:
                ai_score -= 1

        bot.send_message(message.chat.id, f"You answered: {message.text[1:]}\nAI answered: {predicted}\n\nThe right answer is: {correct}")

        bot.send_message(message.chat.id, f"Your score is: {score} \nAI's score is: {ai_score}")


print("Bot is up!")

try:
    bot.infinity_polling(timeout=1000000, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=1000000, long_polling_timeout=5)
