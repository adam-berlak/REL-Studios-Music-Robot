import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re

with open("myfile.txt","w") as myfile:
    for i in range(2741,4096):
        print(str(i))
        res = requests.get("https://ianring.com/musictheory/scales/" + str(i))
        soup = BeautifulSoup(res.content,'lxml')

        name = soup.find("div",attrs={"class":"container"}).findAll("h1")[0]
        print(str(name))
        data = []

        scale_name = re.findall(r'\s"(.*)"', str(name))
            
        if (len(scale_name) == 0):
            scale_name = re.findall('>(\w+\s\d+)<', str(name))[0]
        else:
            scale_name = scale_name[0]

            data.append(scale_name)

        myfile.write(str(i) + ": " + str(scale_name) + "\n")
    

