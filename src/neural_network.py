from os import path
import matplotlib.pyplot as plt

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

from dataloader import JS_Dataset
from webscrape import Webscrape


class JS_Classifier(JS_Dataset, Webscrape):
    def __init__(self):
        super().__init__()

        self.trainset = torch.utils.data.DataLoader(
            dataset = self,
            batch_size = 4,
            shuffle = True
        )

        self.device = "cpu"
        self.model = self.NN().to(self.device)

        self.loss_fn = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr = 1e-3)

        self.loss_history = []

    def train(self):
        size = len(self.trainset.dataset)
        self.model.train()

        epoch_loss = []
        for c, (x, y) in enumerate(self.trainset):
            x, y = x.to(self.device), y.to(self.device)

            # Compute prediction error
            pred = self.model(x)
            loss = self.loss_fn(pred, y)
            epoch_loss.append(loss.item())

            # Backpropagation
            loss.backward()
            self.optimizer.step()
            self.optimizer.zero_grad()

            if c % 4 == 0:
                loss, current = loss.item(), (c + 1) * len(x)
                print(f"loss: {loss:>7f}  [{current:>2d}/{size:>2d}]")

        return epoch_loss

    def learn(self, epochs=10, filename="../models/model.pth", imgname="../graphs/loss.png", save=True):
        if not path.isfile(filename):
            for i in range(epochs):
                print(f"\n-------------------------------Epoch {i+1}")
                epoch_loss = self.train()
                self.loss_history.append(sum(epoch_loss) / len(epoch_loss))

            print("Training finished!")

            if save:
                torch.save(self.model.state_dict(), filename)
                print("Model saved to", filename)

            if imgname != "":
                plt.plot(range(epochs), self.loss_history)
                plt.title("Loss")

                plt.savefig(imgname)
                print("Loss graph successfully saved")

                plt.show()

    def test(self):
        size = len(self.trainset.dataset)
        num_batches = len(self.trainset)
        self.model.eval()

        test_loss, correct = 0, 0

        with torch.no_grad():
            for x, y in self.trainset:
                x, y = x.to(self.device), y.to(self.device)
                pred = self.model(x)

                test_loss += self.loss_fn(pred, y).item()
                correct += (pred.argmax(1) == y.argmax(1)).type(torch.float).sum().item()

            test_loss /= num_batches
            correct /= size

            print(f"Test result: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

    def load(self, filename="../models/model.pth"):
        self.model = self.NN().to(self.device)
        self.model.load_state_dict(torch.load(filename, weights_only=True))

    def predict(self, idx, classes, imgs_dir="../data/images/", plot=True):
        self.model.eval()

        x = self.trainset.dataset[idx][0]
        y = self.trainset.dataset[idx][1].argmax()

        with torch.no_grad():
            x = x.to(self.device)
            pred = self.model(x)
            predicted, actual = classes[pred[0].argmax(0)], classes[y]

            title = f'Predicted: "{predicted}", Actual: "{actual}"'
            if plot:
                self.open_image_file(actual, title, imgs_dir)

            return predicted

    def show_model(self):
        return self.NN().to(self.device)

    class NN(nn.Module):
        def __init__(self):
            super().__init__()

            self.flatten = nn.Flatten()
            self.stack = nn.Sequential(
                nn.Linear(64*64, 2048),
                nn.ReLU(),
                nn.Linear(2048, 1024),
                nn.ReLU(),
                nn.Linear(1024, 512),
                nn.ReLU(),
                nn.Linear(512, 92),

                # nn.Conv2d(in_channels=1, out_channels=64, kernel_size=4),
                # nn.ReLU(),
                # nn.MaxPool2d(kernel_size=2),

                # nn.Conv2d(64, 128, 4),
                # nn.ReLU(),
                # nn.MaxPool2d(kernel_size=2),

                # nn.Conv2d(128, 256, 4),
                # nn.ReLU(),
                # nn.MaxPool2d(kernel_size=2),

                # nn.Flatten(),
                # nn.Linear(6400, 2048),
                # nn.ReLU(),
                # nn.Linear(2048, 1024),
                # nn.ReLU(),
                # nn.Linear(1024, 92),
            )

        def forward(self, x):
            x = self.flatten(x)
            x = self.stack(x)
            return x
