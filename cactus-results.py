import os, bs4, requests, re
import pandas as pd

PATH = os.path.join("C:\\","Users","barry.forrest","Documents","Python Scripts")

res = pd.DataFrame()
url = "http://www.lubbockhomebrew.com/cactus/"
#url = "http://www.lubbockhomebrew.com/cactus/2015"
counter = 0
catExpression = re.compile('(.+)(\(.+\))')

page = requests.get(url)

def div_to_table(div):
    category = div.find('h3')
    m = catExpression.match(category.text)
    if(m != None):
        data = {'category': [ m.group(1)],
                'count': [m.group(2)]}
        return pd.DataFrame(data)

# def table_to_df(table):
#     cats = table.findAll('')
#     return pd.DataFrame([[h3.text for h3 in item.findAll('h3')] for item in table.findAll('div')])


#while True:
print(counter)
soup = bs4.BeautifulSoup(page.content, 'lxml')
cats = soup.findAll(name='div', attrs={'class': 'bcoem-winner-table'})
#res.append({"category":[], "entries": []})
for c in cats:
    res = res.append(div_to_table(c))

res.to_csv(os.path.join(os.path.join(PATH,"cactus-18.csv")), index=False)