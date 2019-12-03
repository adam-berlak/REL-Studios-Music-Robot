import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re

with open("dictionary.txt","w") as dictionary:
    with open('myfile2.txt') as readfile:
        lines = readfile.readlines()

        for line in lines:
            result = re.findall(r'(\d+):\s(.+)', str(line))[0]
            print(result)
            dictionary.write(str(result[1]).replace(" ", "_").replace("-", "_").replace("\\", "_") + " = " + str(result[0]) + "\n")

        
    

