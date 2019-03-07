import os, bs4, requests, re
import pandas as pd

PATH = os.path.join("C:\\","Users","barry.forrest","Documents","Python Scripts")

res = pd.DataFrame()

url = "http://www.lubbockhomebrew.com/cactus/2014"
counter = 0
catExpression = re.compile('(.+)(\(.+\))')

def div_to_table(div):
    m = catExpression.match(div.text)
    if(m != None):
        data = {'category': [ m.group(1)],
                'count': [m.group(2)]}
        return pd.DataFrame(data)

# def table_to_df(table):
#     cats = table.findAll('')
#     return pd.DataFrame([[h3.text for h3 in item.findAll('h3')] for item in table.findAll('div')])


#while True:
print(counter)
page = requests.get(url)
soup = bs4.BeautifulSoup(page.content, 'lxml')
cats = soup.findAll('td', attrs={'class': 'xl66'})
#res.append({"category":[], "entries": []})
for c in cats:
    res = res.append(div_to_table(c))

res.to_csv(os.path.join(os.path.join(PATH,"cactus-14.csv")), index=False)