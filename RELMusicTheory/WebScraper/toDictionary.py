import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re

with open("dictionary.txt","w") as dictionary:
    with open('myfile.txt') as readfile:
        lines = readfile.readlines()

        for line in lines:
            result = re.findall(r'(\d+):\s(.+)', str(line))[0]
            print(result)
            dictionary.write(str(result[0]) + ": " + "\"" + str(result[1]) + "\",\n")

    '''
    for i in range(0,2742):
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
        '''

        
    

