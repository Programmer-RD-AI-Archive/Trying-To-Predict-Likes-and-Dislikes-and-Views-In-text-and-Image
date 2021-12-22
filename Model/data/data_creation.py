import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import os
import wandb
import nltk
from nltk.stem.porter import *
from torch.nn import *
from torch.optim import *
import numpy as np
import pandas as pd
import torch, torchvision
import random
from tqdm import *
from torch.utils.data import Dataset, DataLoader
import cv2, json, threading
from tqdm import tqdm

stemmer = PorterStemmer()
ignore_files = ["analysis.ipynb", ".ipynb_checkpoints", "data_creation.py"]
data1 = pd.read_csv("./US_youtube_trending_data.csv")
data2 = pd.read_csv("./USvideos.csv")
files = list(os.listdir("./"))
files.remove("US_youtube_trending_data.csv")
files.remove("USvideos.csv")
files.remove(".ipynb_checkpoints")
files.remove("analytics.ipynb")
files.remove("data_creation.py")
files.remove(".virtual_documents")
for file in tqdm(files):
    if len(file.split("_")) > 1:
        data1 = data1.append(pd.read_csv(f"./{file}"))
    else:
        data2 = data2.append(pd.read_csv(f"./{file}", encoding="latin-1"))
data1.rename(
    columns={
        "publishedAt": "publish_time",
        "channelTitle": "channel_title",
        "categoryId": "category_id",
        "view_count": "views",
    },
    inplace=True,
)
data = data1.append(data2)
publish_times = []
for publish_time in tqdm(data["publish_time"]):
    publish_time = publish_time.split("-")
    publish_time[2] = publish_time[2][:2]
    publish_time = publish_time[0] + " " + publish_time[1] + " " + publish_time[2]
    publish_times.append(publish_time)
trending_dates = []
for trending_date in tqdm(data["trending_date"]):
    try:
        trending_date = trending_date.split("-")
        trending_date[2] = trending_date[2][:2]
    except:
        trending_date = trending_date[0].split(".")
        trending_date[2] = trending_date[2][:2]

    trending_date = trending_date[0] + " " + trending_date[1] + " " + trending_date[2]
    trending_dates.append(trending_date)
data["trending_date"] = trending_dates
data.to_csv("./data.csv")
