import urllib2
from bs4 import BeautifulSoup
import sqlite3
import datetime

page = 'http://mmapayout.com/blue-book/pay-per-view/'
html = urllib2.urlopen(page)
shtml = BeautifulSoup(html, 'html.parser' )

db = sqlite3.connect("ufcdb")
cursor = db.cursor()


def insertMain(item):
    cursor.execute('''INSERT INTO ppv_nums(event_date, event, main_event, ppv)
                  VALUES(?,?,?,?)''', (datetime.datetime.strptime(item[0], '%m/%d/%Y').strftime('%Y-%m-%d'),item[1], item[2], int(item[3].replace(',','')) ) )
    print("successfully inserted "+ str(item) )
    db.commit()

cursor.execute(''' DELETE FROM ppv_nums''')
db.commit()

rawData = shtml.find_all('td')
data = []
for i in rawData:
    if i.text.strip() != "":
        if i.text.strip() == 'Canceled':
            data.append('0')
        else:
            data.append(i.text.strip())
data = data[4:]

group = []
for x in range(len(data)):
    group.append(data[x])
    if (x+1)%4 == 0:
        insertMain(group)
        group = []

cursor.execute('''SELECT event_date, event, main_event, ppv from ppv_nums where ppv > 500000''')
all_rows = cursor.fetchall()
for row in all_rows:
    # row[0] returns the first column in the query (name), row[1] returns email column.
    print('{0} : {1}, {2}, {3}'.format(row[0], row[1], row[2], row[3]))

db.close()
