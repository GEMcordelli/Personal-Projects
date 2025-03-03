import pandas as pd
import numpy as np
import os
import requests
from io import StringIO
import matplotlib

filenames = ["Amanda.csv", "BabyGotBack.csv", "Ben.csv", "Bump,Bump,Bump.csv",  "DukeOfEarl.csv", "GetBusy.csv", "HelpMe,Rhonda.csv","LetMeLoveYou.csv", "MyLove.csv","OnlyGirlInTheWorld.csv", "PennyLane.csv", "ShakeItOff.csv", "SlowJamz.csv", "TheStreak.csv"]

git = "https://github.com/GEMcordelli/Personal-Projects/tree/main/Artists/Songs"

combined = []

for file in filenames:
    read = pd.read_csv(file)
    combined.append(read)
    
    
    
    
combined = pd.concate(combined)


file - pd.read_csv("Amanda.csv")

getwd()
