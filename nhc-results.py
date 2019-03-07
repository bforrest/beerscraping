import os, bs4, requests, re, csv
import pandas as pd

PATH = os.path.join("C:\\","Users","barry.forrest","Documents","Python Scripts")

contestSites = pd.DataFrame()
results = pd.DataFrame()

contestYears = {}

mainUrl = "https://www.homebrewersassociation.org/national-homebrew-competition/winners/"
dataUrl = "https://www.homebrewersassociation.org/wp-admin/admin-ajax.php"
# ul#year_select to get years
# center-toggle <ul id="center_select" class="dropdown-menu"> has center list

def years_from_listItems(listItems):
    items = listItems.findAll('a')
    years = list()
    for item in items:
        years.append(item.text)
    return years

def judging_centers_for_year(year):
    payload = {'action': 'show_judging_centers', 'year': year}
    r = requests.post(dataUrl, data=payload)
    broth = bs4.BeautifulSoup(r.content, 'lxml')
    facilities = broth.findAll('li')
    sites = []
    for fac in facilities:
        sites.append( { 'id': fac['data-center-id'], 'name': fac['data-center-name']})
    
    return sites

# html sample
# <h3 class='category'>Category 1 : Pale American Beer</h3>
#  <cite class='sponsor'>Sponsored by : 
#     <a href='http://www.fivestarchemicals.com/' target='_blank'>Five Star Chemicals & Supply, Inc.</a> 315 Entries
# </cite>    
def get_winners(year, siteId):
    payload = {'action': 'search_winners', 'center': siteId, 'year': year}
    r = requests.post(dataUrl, data=payload)
    # expected = """<div class="winners">
    # <h3 class='category'>Category 1 : Pale American Beer</h3>
    # <cite class='sponsor'>Sponsored by : <a href='http://www.fivestarchemicals.com/' target='_blank'>Five Star Chemicals & Supply, Inc.</a> 315 Entries</cite>
    # <h3 class="category">Category 20 : Sour Ale</h3>
    # <cite class="sponsor">Sponsored by : <a href="http://www.CaptainLawrenceBrewing.com&#10;" target="_blank">Captain Lawrence Brewing Co.</a> 249 Entries</cite>
    # </div>"""
    page = bs4.BeautifulSoup(r.content, 'lxml')
    winners = page.find('div', {'class': 'winners'})
    category = winners.find("h3")
    localFrame = pd.DataFrame()
    while category != None:
        entries = category.find_next("cite")
        print(category)
        print(entries)
        if entries is not None:
            data = {'category': category.contents, 'entries': entries.text}
            localFrame = localFrame.append(pd.DataFrame(data))
        category = category.findNext("h3")
    return localFrame

# startPage = requests.get(mainUrl)
# soup = bs4.BeautifulSoup(startPage.content, 'lxml')
# years = years_from_listItems(soup.find(id="year_select"))
# print(years)
#years = ['2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003']
# for year in years:
#     sites = judging_centers_for_year(year)
#     contestYears[year] = sites
#     data = {'year': year, 'sites': sites}
#     contestSites = contestSites.from_dict(data)
# print(contestYears)
years = ['2014', '2015', '2016', '2017', '2018']
# contestSites.to_csv(os.path.join(os.path.join(PATH,"contest-sites-by-year.csv")), index=False)
for year in years:
    #sites = contestYears[year]
    results = results.append(get_winners(year, 13))

# for item in contestYears:
#     for site in contestYears[item]:
#         winners = get_winners(item, site['id'])

#contestSites.to_csv(os.path.join(os.path.join(PATH,"contest-sites-by-year.csv")), index=False)
results.to_csv(os.path.join(os.path.join(PATH,"2014-and-beyond-national-finals.csv")), index=False)