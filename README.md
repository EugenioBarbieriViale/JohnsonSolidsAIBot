# @JohnsonSolidsAIBot
JohnsonSolidsAIBot is a Telegram bot which you can challenge in recognising Johnson solids. I webscraped the images of the 92 Johnson solids from Wikipedia and trained a Neural Network that is able to classify them, and given the image recognises the name of the solid. Can you beat it?

There are different versions of the model, from veary easy (trained with only 100 epochs, with 85.9% accuracy) to impossible (2500 epochs, 100.0% accuracy)

More information about Johnson solids [here](https://en.wikipedia.org/wiki/Johnson_solid)

## Triaugmented truncated dodecahedron
![image](https://github.com/user-attachments/assets/64fd6c7f-814e-4876-96c2-7033a8de42cd)

## Python dependencies
- numpy
- pandas
- matplotlib
- pytorch
- torchvision
- requests
- beautiful soup
- cairosvg
- cv2
- pyTelegramBotAPI
