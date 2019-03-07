import os, bs4, requests, re, csv
import pandas as pd

PATH = os.path.join("C:\\","Users","barry.forrest","Documents","Python Scripts")

with open("2018-NationalResults.html") as fp:
    data = fp.read()

res = pd.DataFrame()

soup = bs4.BeautifulSoup(data, 'lxml')

winners = soup.find('div', {'class': 'winners'})

category = winners.find("h3")

while category != None:
    entries = category.find_next("cite")
    print(category)
    print(entries)
    if entries is not None:
        data = {'category': category.contents, 'entries': entries.text}
        res = res.append(pd.DataFrame(data))
    category = category.findNext("h3")
    
print("done")
res.to_csv(os.path.join(os.path.join(PATH,"nationals-from-file.csv")), index=False)