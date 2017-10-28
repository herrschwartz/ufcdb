import urllib2
from bs4 import BeautifulSoup
import codecs

page = 'http://www.officetally.com/the-office-episode-list-guide'
#these next two lines are needed for sites that don't allow direct acces and 403
req = urllib2.Request(page, headers={'User-Agent' : "Magic Browser"})
html = urllib2.urlopen( req )
shtml = BeautifulSoup(html, 'html.parser' )

rawData = shtml.find('div', {'class' : "entry-content"})
lis = rawData.find_all('li')


f = codecs.open('episode_data', 'w', encoding="utf-8")
for i in lis:
    l = i.get_text()
    l = l[6:]
    if "-" in l and "Cover" not in l:
        l = l[4:]
        x = l[:8].split(".")
        x[1].lstrip(" 0")
        l = l[8:]
        string = "Season " + x[0] + " Episode " + x[1] + "- " + l+",\n"
    else:
        x = l[:5].split(".")
        x[1].lstrip(" 0")
        l = l[5:]
        string = "Season " + x[0] + " Episode " + x[1] + "- " + l+",\n"
    f.write(string)

f.close()
