import io
from time import sleep

import matplotlib.pyplot as plt
from matplotlib import image as mpimg

from csv import writer
import cairosvg

import requests
from bs4 import BeautifulSoup


class Webscrape:
    def __init__(self):
        self.url = "https://en.wikipedia.org/wiki/List_of_Johnson_solids"

        self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    def call(self):
        self.s = requests.Session()
        self.r = self.s.get(self.url, headers=self.headers)

        self.soup = BeautifulSoup(self.r.content, "html.parser")

    def get_names(self):
        self.call()
        all_td = self.soup.find_all("td")

        names = []
        for t in all_td:
            a = t.a
            if a is not None and "href" in a.attrs and "title" in a.attrs:
                if a.text[0].isupper():
                    names.append([a.text])

        return names

    def download_images(self, _dir):
        # Elongated_triangular_gyrobicupola.png

        self.call()
        all_img = self.soup.find_all("img", class_="mw-file-element")

        images = []
        i = 0
        for a in all_img:
            if "commons" in a["src"]:
                img_url = "https:" + a["src"]

                img_url = img_url.replace("thumb/", "")
                img_url = img_url.split("/120", 1)[0]

                name = img_url[52:]
                name = name.replace(".svg", ".png")

                print(f"{i}:", name)
                i += 1

                response = requests.get(img_url, stream = True, headers=self.headers)
                sleep(5)
                
                if response.status_code != 200:
                    print(f"! Failed to download {img_url} (HTTP {response.status_code})")

                if ".svg" in img_url:
                    img_data = cairosvg.svg2png(response.content)
                else:
                    img_data = response.content

                filename = _dir + name
                with open(filename, 'wb') as file:
                    file.write(img_data)

    def open_image_file(self, name, title, _dir):
        if "bipyramid" in name:
            name = name.replace("bipyramid", "dipyramid")

        filename = _dir + name.replace(" ", "_") + ".png"

        img = plt.imread(filename, format="PNG")
        plt.title(title)
        plt.imshow(img)
        plt.show()

    def open_image_request(self, img_url):
        response = requests.get(img_url, stream = True, headers=self.headers)
        
        if response.status_code != 200:
            print(f"! Failed to download {img_url} (HTTP {response.status_code})")

        img = io.BytesIO(response.content)
        img = plt.imread(img, format="PNG")
        plt.imshow(img)
        plt.show()

    def save(self, file_path, array):
        with open(file_path, mode="w", newline="") as file:
            w = writer(file)
            w.writerows(array)
