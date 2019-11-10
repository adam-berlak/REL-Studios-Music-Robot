import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

with open("myfile.txt","w") as myfile:
    for i in range(2741,2742):
        print(str(i))
        res = requests.get("https://ianring.com/musictheory/scales/" + str(i))
        soup = BeautifulSoup(res.content,'lxml')
        #try:
        table = soup.find("div",attrs={"class":"modes"}).findAll("table")[0]
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        myfile.write(str(i) + ": " + str(data) + "\n")

        rows2 = soup.find("div",attrs={"class":"row"}).find("div",attrs={"class":"col-md-7"})
        '''
        for row in rows:
            cells = row.find_all("td")
            rn = cells[0].get_text()
            myfile.write(str(rn) + "\n")
            '''
        #except:
        #    print("table not found")
    

